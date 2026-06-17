from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.routers.main import router as main_router
from app.routers.user import router as user_router
from app.routers.cafe import router as cafe_router
from app.routers.menu_category import router as menu_category_router
from app.routers.dish import router as dish_router
from app.routers.delivery_zone import router as delivery_zone_router
from app.routers.order import router as order_router
from app.routers.stripe_router import router as stripe_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.ENVIRONMENT == "development"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Роутеры
app.include_router(main_router)
app.include_router(user_router)
app.include_router(cafe_router)
app.include_router(menu_category_router)
app.include_router(dish_router)
app.include_router(delivery_zone_router)
app.include_router(order_router)
app.include_router(stripe_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
