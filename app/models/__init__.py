# app/models/__init__.py  — ОБНОВЛЁННАЯ ВЕРСИЯ
# Импортируем все модели чтобы Alembic их видел при автогенерации миграций

from app.models.user import User
from app.models.cafe import Cafe
from app.models.menu_category import MenuCategory
from app.models.dish import Dish
from app.models.delivery_zone import DeliveryZone
from app.models.stripe_account import StripeAccount
from app.models.order import Order
from app.models.order_item import OrderItem

__all__ = [
    "User",
    "Cafe",
    "MenuCategory",
    "Dish",
    "DeliveryZone",
    "StripeAccount",
    "Order",
    "OrderItem",
]