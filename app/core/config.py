from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "FoodFlow"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "super-secret-key-change-me-in-production"

    # Database — SQLite для локальной разработки (очень важно сейчас)
    DATABASE_URL: str = "sqlite:///./foodflow.db"

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()