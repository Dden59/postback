import os

# Обязательные параметры
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1002665040288))  # Ваш канал для постбеков
PARTNER_LINK = os.getenv("PARTNER_LINK", "https://1wwcr.com/").rstrip('/') + '/'
WEBAPP_LINK = os.getenv("WEBAPP_LINK", "https://dden59.github.io/keeper/")

# Жёсткие проверки
assert len(BOT_TOKEN) == 46, "Неверная длина токена! Проверьте BOT_TOKEN"
assert CHANNEL_ID < 0, "CHANNEL_ID должен быть отрицательным (канал/супергруппа)"
assert WEBAPP_LINK.startswith('https://'), "WebApp требует HTTPS!"
