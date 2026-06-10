from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.routers.main import router as main_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.ENVIRONMENT == "development"
)

# Монтируем статику
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры
app.include_router(main_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}