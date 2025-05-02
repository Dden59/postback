import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, PARTNER_LINK, WEBAPP_LINK, CHANNEL_ID
from utils import wait_for_event

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
users_in_progress = {}

# Клавиатуры
def get_registration_kb(user_id: int):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "🔹 Зарегистрироваться", 
            url=f"{PARTNER_LINK}{user_id}"
        )
    )

def get_deposit_kb(user_id: int):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "💰 Сделать первый депозит", 
            url=f"{PARTNER_LINK}{user_id}"
        )
    )

def get_app_access_kb():
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "🚀 Открыть Rocket Keeper", 
            web_app=types.WebAppInfo(url=WEBAPP_LINK)
        )
    )

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    
    if not str(user_id).isdigit():
        await message.answer("❌ Ошибка: неверный ID пользователя")
        return

    users_in_progress[user_id] = {"reg": False, "dep": False}
    
    # Первый этап - регистрация
    await message.answer(
        "📝 Для доступа к Rocket Keeper вам нужно:\n\n"
        "1. Зарегистрироваться на платформе\n"
        "2. Сделать депозит от 500 RUB\n\n"
        "Нажмите кнопку ниже чтобы начать:",
        reply_markup=get_registration_kb(user_id)
    )

    # Ожидаем регистрацию (формат: {user_id})
    try:
        registered = await wait_for_event(bot, user_id, "Lead", timeout=600)
        if not registered:
            await message.answer("⌛ Время ожидания регистрации истекло. Попробуйте снова /start")
            return

        users_in_progress[user_id]["reg"] = True
        
        # Второй этап - депозит (формат: {user_id}|Firstdep|{amount})
        await message.answer(
            "✅ Регистрация подтверждена!\n\n"
            "Теперь сделайте первый депозит от 500 RUB:",
            reply_markup=get_deposit_kb(user_id)
        )

        deposit_amount = await wait_for_event(bot, user_id, "Firstdep", timeout=600)
        if not deposit_amount:
            await message.answer("⌛ Время ожидания депозита истекло. Попробуйте снова /start")
            return

        if deposit_amount < 500:
            await message.answer(
                f"❌ Сумма депозита {deposit_amount} RUB меньше минимальной (500 RUB)\n"
                "Попробуйте снова /start"
            )
            return

        users_in_progress[user_id]["dep"] = True
        
        # Финальный этап - доступ к приложению
        await message.answer(
            f"🎉 Поздравляем! Ваш депозит {deposit_amount} RUB подтверждён.\n\n"
            "Теперь вы можете использовать Rocket Keeper:",
            reply_markup=get_app_access_kb()
        )

    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
