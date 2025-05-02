import os

# Основные настройки
BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
CHANNEL_ID = -1002665040288
WEBAPP_URL = "https://dden59.github.io/keeper/"

# Автоматическое определение домена
DOMAIN = f"https://{os.getenv('RAILWAY_PROJECT_NAME', 'gracious-rebirth')}.up.railway.app"

# Жесткие проверки
assert BOT_TOKEN and len(BOT_TOKEN) == 46, "Неверный токен бота!"
assert str(CHANNEL_ID).startswith("-100"), "CHANNEL_ID должен быть ID канала"
assert DOMAIN.startswith('https://'), f"Требуется HTTPS! Текущий домен: {DOMAIN}"
