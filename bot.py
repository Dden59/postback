import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from utils import wait_for_event

BOT_TOKEN = "7554184368:AAFppJytJDqR2Ssw8fTnQ9_IRvURLcG2lU8"
DOMAIN = f"https://{os.getenv('RAILWAY_PROJECT_NAME', 'gracious-rebirth')}.up.railway.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"
WEBAPP_URL = "https://dden59.github.io/keeper/"
POSTBACK_CHANNEL_ID = -1002665040288

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Хранилище статуса пользователей (в памяти)
user_status = {}

@dp.message(commands=["start"])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"/start от {user_id}")

    # Отправляем ссылку на регистрацию
    link = f"https://1wwcr.com/?sub1={user_id}"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(text="🚀 Зарегистрироваться", url=link)
        ]]
    )
    await message.answer(
        "👋 Добро пожаловать в <b>Rocket Keeper</b>!\n\nЧтобы начать, зарегистрируйтесь на платформе:",
        reply_markup=keyboard
    )

    user_status[user_id] = {"lead": False, "deposit": False}

@dp.channel_post()
async def handle_postback(message: types.Message):
    if message.chat.id != POSTBACK_CHANNEL_ID or not message.text:
        return

    text = message.text.strip()

    if "|Firstdep|" in text:
        try:
            user_id, _, amount = text.split("|")
            user_id = int(user_id)
            amount = float(amount)

            if user_id in user_status:
                user_status[user_id]["deposit"] = True

                keyboard = types.InlineKeyboardMarkup(
                    inline_keyboard=[[
                        types.InlineKeyboardButton(text="🎮 Открыть Rocket Keeper", web_app=types.WebAppInfo(url=WEBAPP_URL))
                    ]]
                )
                await bot.send_message(
                    chat_id=user_id,
                    text=f"🔥 Депозит {amount:.0f}₽ подтверждён! Добро пожаловать в Rocket Keeper!",
                    reply_markup=keyboard
                )
                logger.info(f"✅ Депозит подтверждён: {user_id} | {amount}")
        except Exception as e:
            logger.error(f"Ошибка при обработке Firstdep: {e}")

    else:
        try:
            user_id = int(text)
            if user_id in user_status:
                user_status[user_id]["lead"] = True
                await bot.send_message(
                    chat_id=user_id,
                    text="🎉 Поздравляем с регистрацией! Теперь внесите депозит, чтобы получить доступ к Rocket Keeper."
                )
                logger.info(f"✅ Лид подтверждён: {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при обработке лида: {e}")

# Health check
async def health_check(request):
    return web.Response(text="OK")

# Запуск
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logger.info(f"🚀 Вебхук установлен: {WEBHOOK_URL}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logger.info("❌ Вебхук удалён")

app = web.Application()
app.router.add_get("/health", health_check)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
