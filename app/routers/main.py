from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.core.deps import get_current_user
from app.models.user import User
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1 style="text-align:center; margin-top:100px; font-family:sans-serif; color:#2563eb;">
        🚀 FoodFlow запущен успешно!<br><br>
        <small>Мультиязычный сервис заказа еды для кафе</small>
    </h1>
    <p style="text-align:center; font-size:18px;">
        <a href="/docs" target="_blank">→ Открыть Swagger документацию</a>
    </p>
    """

@router.get("/me", tags=["auth"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "message": "Авторизация работает!"
    }

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("client/register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("client/login.html", {"request": request})