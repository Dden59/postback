import os
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# 🔐 Вставь токен и домен напрямую
BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
DOMAIN = "https://gracious-rebirth.up.railway.app"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Ответ на /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("✅ Бот работает! Ты получил это сообщение 🎉")
    logger.info(f"💬 Ответили на /start от {message.from_user.id}")

# Ловим любые другие сообщения
@dp.message_handler()
async def all_handler(message: types.Message):
    await message.reply("📩 Принято сообщение!")
    logger.info(f"📩 Сообщение от {message.from_user.id}: {message.text}")

# webhook endpoint
async def webhook_handler(request):
    try:
        data = await request.json()
        logger.info(f"📥 RAW: {data}")
        update = types.Update.to_object(data)
        await dp.process_update(update)
        return web.Response(text="ok")
    except Exception as e:
        logger.error(f"❌ Ошибка в webhook: {e}")
        return web.Response(status=500)

# health-check
async def health_check(request):
    return web.Response(text="OK")

# старт и стоп
async def on_startup(app):
    await bot.set_webhook(f"{DOMAIN}/webhook", drop_pending_updates=True)
    logger.info("🚀 Webhook установлен")

async def on_shutdown(app):
    await bot.delete_webhook()
    logger.info("❌ Webhook удалён")

# aiohttp app
def create_app():
    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)
    app.router.add_get("/health", health_check)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)
