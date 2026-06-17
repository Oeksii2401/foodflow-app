import secrets
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.core.deps import get_current_active_user
from app.core.telegram import notify_new_order
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    subtotal = 0.0
    items_data = []
    for item in data.items:
        dish = db.query(Dish).filter(Dish.id == item.dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish {item.dish_id} not found")
        if not dish.is_available:
            raise HTTPException(status_code=400, detail=f"Dish '{dish.name}' is not available")
        subtotal += dish.price * item.quantity
        items_data.append((dish, item.quantity))

    delivery_price = 0.0
    if data.delivery_zone_id:
        from app.models.delivery_zone import DeliveryZone
        zone = db.query(DeliveryZone).filter(DeliveryZone.id == data.delivery_zone_id).first()
        if zone:
            delivery_price = zone.delivery_price

    order = Order(
        cafe_id=data.cafe_id,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        customer_email=data.customer_email,
        delivery_address=data.delivery_address,
        delivery_lat=data.delivery_lat,
        delivery_lng=data.delivery_lng,
        delivery_zone_id=data.delivery_zone_id,
        delivery_price=delivery_price,
        subtotal=subtotal,
        total=subtotal + delivery_price,
        comment=data.comment,
        language=data.language,
        qr_code=secrets.token_urlsafe(16),
    )
    db.add(order)
    db.flush()

    for dish, quantity in items_data:
        order_item = OrderItem(
            order_id=order.id,
            dish_id=dish.id,
            dish_name=dish.name,
            dish_price=dish.price,
            quantity=quantity,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    # Уведомление в Telegram
    await notify_new_order(order)

    return order


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/cafe/{cafe_id}", response_model=list[OrderRead])
def list_cafe_orders(
    cafe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Order).filter(Order.cafe_id == cafe_id).order_by(Order.created_at.desc()).all()


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.status
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/confirm-qr", response_model=OrderRead)
def confirm_order_qr(order_id: int, qr_code: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.qr_code != qr_code:
        raise HTTPException(status_code=400, detail="Invalid QR code")
    order.is_confirmed = True
    order.status = "delivered"
    db.commit()
    db.refresh(order)
    return order
