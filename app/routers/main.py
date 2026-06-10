from fastapi import APIRouter
from fastapi.responses import HTMLResponse

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