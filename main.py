from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FoodFlow")

# Подключаем папки
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home():
    return {"message": "FoodFlow работает! 🚀"}

print("Сервер FoodFlow запущен!")