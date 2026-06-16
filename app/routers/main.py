from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.cafe import Cafe
from app.models.menu_category import MenuCategory
from app.models.dish import Dish
from app.models.order import Order

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return HTMLResponse("""
    <h1 style="text-align:center; margin-top:100px; font-family:sans-serif; color:#2563eb;">
        FoodFlow
    </h1>
    <p style="text-align:center; font-size:18px;">
        <a href="/menu/1">/menu/1</a> &nbsp;|&nbsp;
        <a href="/admin/setup">/admin/setup</a> &nbsp;|&nbsp;
        <a href="/docs">/docs</a>
    </p>
    """)


@router.get("/menu/{cafe_id}", response_class=HTMLResponse)
async def menu_page(cafe_id: int, request: Request, db: Session = Depends(get_db)):
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id, Cafe.is_active == True).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    categories = db.query(MenuCategory).filter(MenuCategory.cafe_id == cafe_id).order_by(MenuCategory.sort_order).all()
    dishes = db.query(Dish).filter(Dish.cafe_id == cafe_id, Dish.is_available == True).order_by(Dish.sort_order).all()
    return templates.TemplateResponse(request=request, name="client/menu.html", context={
        "cafe": cafe,
        "categories": categories,
        "dishes": dishes,
        "lang": request.query_params.get("lang", "de"),
    })


@router.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    return templates.TemplateResponse(request=request, name="client/cart.html", context={
        "lang": request.query_params.get("lang", "de"),
    })


@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse(request=request, name="client/checkout.html", context={
        "lang": request.query_params.get("lang", "de"),
    })


@router.get("/order/{order_id}", response_class=HTMLResponse)
async def order_status_page(order_id: int, request: Request, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return templates.TemplateResponse(request=request, name="client/order_status.html", context={
        "order": order,
        "lang": request.query_params.get("lang", "de"),
    })


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="client/register.html")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="client/login.html")


@router.get("/me", tags=["auth"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
    }


@router.get("/admin/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin/setup.html")
