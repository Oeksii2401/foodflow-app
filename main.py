from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="FoodFlow", version="0.1.0")

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1 style="text-align:center; margin-top:100px; font-family:sans-serif;">
        🚀 FoodFlow запущен успешно!<br><br>
        <small>Мультиязычный сервис заказа еды</small>
    </h1>
    <p style="text-align:center;">
        <a href="/docs" style="font-size:18px;">→ Перейти в Swagger документацию</a>
    </p>
    """

@app.get("/health")
async def health():
    return {"status": "healthy"}