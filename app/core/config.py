from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "FoodFlow"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "change-this-in-production"
    
    # База данных
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/foodflow"
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    
    # Другие
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()