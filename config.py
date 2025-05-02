import os

# Все значения получаются из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Берется из Railway
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1002665040288))  # Значение по умолчанию уже новое!
PARTNER_LINK = os.getenv("PARTNER_LINK", "https://1wwcr.com/?sub1=")
WEBAPP_LINK = os.getenv("WEBAPP_LINK", "https://dden59.github.io/keeper/")
