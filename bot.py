import logging
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web
from config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL, DOMAIN
from utils import wait_for_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# /start — приветствие
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    registration_link = f"https://1wwcr.com/?sub1={user_id}"

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("🚀 Зарегистрироваться", url=registration_link)
    )

    await message.answer(
        "👋 Привет! Чтобы начать пользоваться приложением <b>Rocket Keeper</b>, тебе нужно зарегистрироваться 👇",
        parse_mode="HTML",
        reply_markup=keyboard
    )

    # Ожидаем регистрацию
    registered = await wait_for_event(bot, user_id, event_type="Lead")
    if registered:
        await message.answer(
            "🎉 Поздравляем с регистрацией!\n💸 Теперь внесите депозит, чтобы получить доступ к приложению Rocket Keeper."
        )

        # Ожидаем депозит
        deposit_amount = await wait_for_event(bot, user_id, event_type="Firstdep")
        if deposit_amount:
            keyboard = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🎮 Перейти в Rocket Keeper", web_app=types.WebAppInfo(url=WEBAPP_URL))
            )
            await message.answer(
                f"🔥 Успешный депозит {deposit_amount:.0f}₽ получен!\nДобро пожаловать в Rocket Keeper!",
                reply_markup=keyboard
            )
        else:
            await message.answer("⏳ Ожидание депозита завершилось. Попробуйте снова позже.")
    else:
        await message.answer("⏳ Время ожидания регистрации истекло. Попробуйте снова.")

# Health-check
async def health_check(request):
    return web.Response(text="OK")

# Обработка вебхуков
async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.to_object(data)
        await dp.process_update(update)
        return web.Response()
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)

# Веб-сервер и вебхук
async def on_startup(app):
    await bot.set_webhook(f"{DOMAIN}/webhook", drop_pending_updates=True)
    logger.info("✅ Вебхук установлен!")

async def on_shutdown(app):
    await bot.delete_webhook()
    logger.info("❌ Вебхук удалён!")

def create_app():
    app = web.Application()
    app.router.add_get("/health", health_check)
    app.router.add_post("/webhook", handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
