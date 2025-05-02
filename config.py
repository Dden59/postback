import os

BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
CHANNEL_ID = -1002665040288
WEBAPP_URL = "https://dden59.github.io/keeper/"

# Автоматическое определение домена Railway
RAILWAY_DOMAIN = os.getenv("RAILWAY_STATIC_URL")  # Для продакшена
LOCAL_DOMAIN = "http://localhost:8000"  # Для тестирования

DOMAIN = RAILWAY_DOMAIN or LOCAL_DOMAIN

if not DOMAIN:
    raise ValueError("Не удалось определить домен!")
