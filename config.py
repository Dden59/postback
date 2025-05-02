import os

# Токен бота-обработчика (главный бот)
BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"

# ID канала для постбеков (начинается с -100)
CHANNEL_ID = -1002665040288

# Ссылки (HTTPS обязательно!)
PARTNER_LINK = "https://1wwcr.com/?sub1="
WEBAPP_LINK = "https://dden59.github.io/keeper/"

# Проверки
assert BOT_TOKEN == "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8", "Неверный токен бота!"
assert str(CHANNEL_ID).startswith("-100"), "CHANNEL_ID должен быть ID канала"
