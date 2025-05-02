import logging
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web
from aiogram.utils.executor import start_webhook
from config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL, DOMAIN

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = web.Application()

# Healthcheck для Railway
async def health_check(request):
    return web.Response(text="OK")

# Запуск вебхука
async def on_startup(dp):
    app.router.add_get('/health', health_check)
    
    try:
        await bot.set_webhook(
            url=f"{DOMAIN}/webhook",
            drop_pending_updates=True
        )
        logger.info("✅ Вебхук успешно установлен!")
    except Exception as e:
        logger.error(f"❌ Ошибка при установке вебхука: {e}")
        raise

# Завершение работы
async def on_shutdown(dp):
    await bot.delete_webhook()
    logger.info("Бот остановлен")

# Обработчик сообщений из канала
@dp.channel_post_handler(chat_id=CHANNEL_ID)
async def handle_post(message: types.Message):
    try:
        if "|Firstdep|" in message.text:
            user_id, _, amount = message.text.split('|')
            amount = float(amount)
            
            if amount >= 500:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"✅ Депозит {amount} RUB принят!",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            "🚀 Открыть приложение",
                            web_app=types.WebAppInfo(url=WEBAPP_URL)
                    )
                )
            else:
                logger.warning(f"Маленький депозит: {amount} RUB")
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")

# Точка входа
if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        app=app
    )
