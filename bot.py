import logging
import os
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL, DOMAIN
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Health check для Railway
async def health_check(request):
    return web.Response(text="OK")

# Обработка постбэков из канала
@dp.channel_post_handler(chat_id=CHANNEL_ID)
async def handle_post(message: types.Message):
    try:
        if "|Firstdep|" in message.text:
            user_id, _, amount = message.text.split('|')
            if float(amount) >= 500:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"✅ Депозит {amount} RUB принят!",
                    reply_markup=types.InlineKeyboardMarkup().row(
                        types.InlineKeyboardButton(
                            "🚀 Открыть приложение",
                            web_app=types.WebAppInfo(url=WEBAPP_URL)
                        )
                    )
                )
    except Exception as e:
        logger.error(f"Ошибка при обработке поста: {e}")

# Настройка и запуск aiohttp-сервера
async def on_startup(app):
    await bot.set_webhook(f"{DOMAIN}/webhook", drop_pending_updates=True)
    logger.info("✅ Вебхук установлен!")

async def on_shutdown(app):
    await bot.delete_webhook()

# Создание aiohttp приложения
def create_app():
    app = web.Application()
    app.router.add_get("/health", health_check)
    app.router.add_post("/webhook", dp.router)  # aiogram 3.0+
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
