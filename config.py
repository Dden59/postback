import os

# Обязательные настройки
BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
CHANNEL_ID = -1002665040288
WEBAPP_URL = "https://dden59.github.io/keeper/"

# Автоматическое определение домена
DOMAIN = f"https://{os.getenv('RAILWAY_PROJECT_NAME', 'your-project-name')}.up.railway.app"

# Жёсткая проверка HTTPS
if not DOMAIN.startswith('https://'):
    raise ValueError("Webhook требует HTTPS! Проверьте DOMAIN в config.py")
