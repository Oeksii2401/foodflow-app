import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.cafe import Cafe
from app.models.order import Order
from app.models.stripe_account import StripeAccount
from app.models.user import User

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/stripe", tags=["stripe"])


@router.post("/onboarding/{cafe_id}")
def start_onboarding(
    cafe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Начать onboarding кафе в Stripe Connect."""
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id, Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")

    # Проверяем есть ли уже stripe аккаунт
    stripe_acc = db.query(StripeAccount).filter(StripeAccount.cafe_id == cafe_id).first()

    if not stripe_acc:
        # Создаём новый Express аккаунт
        account = stripe.Account.create(type="express")
        stripe_acc = StripeAccount(
            cafe_id=cafe_id,
            stripe_account_id=account.id,
            is_onboarded=False,
        )
        db.add(stripe_acc)
        db.commit()
        db.refresh(stripe_acc)

    # Создаём ссылку для onboarding
    account_link = stripe.AccountLink.create(
        account=stripe_acc.stripe_account_id,
        refresh_url=f"http://localhost:8000/stripe/onboarding/{cafe_id}/refresh",
        return_url=f"http://localhost:8000/stripe/onboarding/{cafe_id}/complete",
        type="account_onboarding",
    )

    return {"url": account_link.url}


@router.get("/onboarding/{cafe_id}/complete", response_class=HTMLResponse)
def onboarding_complete(cafe_id: int, db: Session = Depends(get_db)):
    """Кафе завершило onboarding."""
    stripe_acc = db.query(StripeAccount).filter(StripeAccount.cafe_id == cafe_id).first()
    if stripe_acc:
        # Проверяем статус аккаунта
        account = stripe.Account.retrieve(stripe_acc.stripe_account_id)
        stripe_acc.is_onboarded = account.details_submitted
        stripe_acc.charges_enabled = account.charges_enabled
        stripe_acc.payouts_enabled = account.payouts_enabled
        db.commit()

    return HTMLResponse("""
    <h1 style="text-align:center; margin-top:100px; font-family:sans-serif; color:#16a34a;">
        ✅ Onboarding завершён!
    </h1>
    <p style="text-align:center;">Кафе подключено к Stripe. Можно принимать платежи.</p>
    <p style="text-align:center;"><a href="/admin/setup">← Назад</a></p>
    """)


@router.get("/onboarding/{cafe_id}/refresh")
def onboarding_refresh(cafe_id: int):
    """Обновить ссылку onboarding если истекла."""
    return RedirectResponse(url=f"/stripe/onboarding/{cafe_id}")


@router.post("/checkout/{order_id}")
def create_checkout(
    order_id: int,
    db: Session = Depends(get_db),
):
    """Создать Stripe Checkout Session для заказа."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    stripe_acc = db.query(StripeAccount).filter(
        StripeAccount.cafe_id == order.cafe_id,
        StripeAccount.is_onboarded == True,
    ).first()

    if not stripe_acc:
        raise HTTPException(status_code=400, detail="Cafe is not connected to Stripe")

    # Комиссия платформы 10%
    platform_fee = int(order.total * 100 * 0.10)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": f"Заказ #{order.id} — {order.cafe.name}"},
                "unit_amount": int(order.total * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"http://localhost:8000/order/{order.id}?paid=true",
        cancel_url=f"http://localhost:8000/order/{order.id}?cancelled=true",
        payment_intent_data={
            "application_fee_amount": platform_fee,
            "transfer_data": {"destination": stripe_acc.stripe_account_id},
        },
    )

    order.stripe_checkout_session_id = session.id
    db.commit()

    return {"url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Обработка Stripe вебхуков."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]

        order = db.query(Order).filter(
            Order.stripe_checkout_session_id == session_id
        ).first()

        if order:
            order.status = "paid"
            order.stripe_payment_intent_id = session.get("payment_intent")
            db.commit()

    return {"status": "ok"}
