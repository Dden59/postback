import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, PARTNER_LINK, WEBAPP_LINK, CHANNEL_ID
from utils import wait_for_event

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота с хранилищем состояний
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
users_in_progress = {}

def get_registration_kb(user_id: int):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "🔹 Зарегистрироваться", 
            url=f"{PARTNER_LINK}{user_id}"
        )
    )

def get_deposit_kb(user_id: int):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "💰 Сделать первый депозит", 
            url=f"{PARTNER_LINK}{user_id}"
        )
    )

def get_app_access_kb():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "🚀 Открыть Rocket Keeper", 
            web_app=types.WebAppInfo(url=WEBAPP_LINK)
        )
    )

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"🔄 Обработка /start для user_id: {user_id}")
    
    try:
        users_in_progress[user_id] = {"reg": False, "dep": False}
        
        # Этап 1: Регистрация
        await message.answer(
            "📝 Для доступа к Rocket Keeper:\n\n"
            "1. Зарегистрируйтесь по кнопке ниже\n"
            "2. Сделайте депозит от 500 RUB\n\n"
            "Я пришлю уведомление после проверки данных",
            reply_markup=get_registration_kb(user_id)
        )

        # Ожидаем регистрацию (10 минут)
        registered = await wait_for_event(bot, user_id, "Lead", timeout=600)
        if not registered:
            await message.answer("⌛ Регистрация не обнаружена. Попробуйте снова /start")
            return

        users_in_progress[user_id]["reg"] = True
        
        # Этап 2: Депозит
        await message.answer(
            "✅ Регистрация подтверждена!\n\n"
            "Теперь сделайте депозит от 500 RUB:",
            reply_markup=get_deposit_kb(user_id)
        )

        deposit_amount = await wait_for_event(bot, user_id, "Firstdep", timeout=600)
        if not deposit_amount:
            await message.answer("⌛ Депозит не обнаружен. Попробуйте снова /start")
            return

        if deposit_amount < 500:
            await message.answer(f"❌ Сумма {deposit_amount} RUB меньше минимальной (500 RUB)")
            return

        users_in_progress[user_id]["dep"] = True
        
        # Этап 3: Доступ
        await message.answer(
            f"🎉 Депозит {deposit_amount} RUB подтверждён!\n"
            "Доступ к приложению:",
            reply_markup=get_app_access_kb()
        )

    except Exception as e:
        logger.error(f"💥 Ошибка: {str(e)}")
        await message.answer("⚠️ Техническая ошибка. Попробуйте позже /start")

@dp.message_handler(commands=["debug"])
async def debug_cmd(message: types.Message):
    """Команда для проверки работы бота"""
    try:
        test_msg = await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"Тест от @Rocket_keeper_robot (user_id: {message.from_user.id})"
        )
        await message.answer(f"✅ Бот работает! Сообщение в канале: ID {test_msg.message_id}")
    except Exception as e:
        await message.answer(f"❌ Ошибка доступа к каналу: {str(e)}")

async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Бот запущен!")

if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=on_startup,
        skip_updates=True,
        timeout=60,
        relax=0.5
    )
