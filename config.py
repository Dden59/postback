import os

BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
CHANNEL_ID = -1002665040288  # ID вашего канала
WEBAPP_URL = "https://dden59.github.io/keeper/"  # HTTPS обязательно!
DOMAIN = os.getenv("RAILWAY_STATIC_URL")  # Автоматически подставится в Railway

# Проверки
assert BOT_TOKEN and len(BOT_TOKEN) == 46, "Неверный токен бота!"
assert str(CHANNEL_ID).startswith("-100"), "CHANNEL_ID должен быть ID канала"
