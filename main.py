from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers.main import router as main_router
from app.routers.user import router as user_router   # ← добавь

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.ENVIRONMENT == "development"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Роутеры
app.include_router(main_router)
app.include_router(user_router)   # ← добавь

@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}