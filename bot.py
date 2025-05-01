import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, PARTNER_LINK, WEBAPP_LINK
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

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    
    # Проверяем валидность user_id
    if not str(user_id).isdigit():
        await message.answer("❌ Ошибка: неверный ID пользователя")
        return

    users_in_progress[user_id] = {"reg": False, "dep": False}
    link = f"{PARTNER_LINK}{user_id}"
    
    await message.answer(
        f"👋 Привет! Для доступа к Rocket Keeper:\n\n"
        f"1. Зарегистрируйтесь по ссылке:\n🔗 {link}\n\n"
        f"2. Сделайте депозит от 500 RUB\n\n"
        f"Я пришлю уведомление после проверки..."
    )

    try:
        # Ожидаем регистрацию (5 минут)
        registered = await wait_for_event(bot, user_id, "Lead")
        if not registered:
            await message.answer("❌ Регистрация не подтверждена. Попробуйте снова.")
            return

        users_in_progress[user_id]["reg"] = True
        await message.answer("✅ Регистрация подтверждена! Теперь сделайте депозит от 500 RUB...")

        # Ожидаем депозит (5 минут)
        deposit_amount = await wait_for_event(bot, user_id, "Firstdep")
        if not deposit_amount:
            await message.answer("❌ Депозит не обнаружен. Попробуйте позже.")
            return

        # Проверяем минимальную сумму депозита
        if deposit_amount < 500:
            await message.answer(f"❌ Сумма депозита {deposit_amount} RUB меньше минимальной (500 RUB)")
            return

        users_in_progress[user_id]["dep"] = True
        
        # Создаем кнопку для мини-приложения
        btn = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "🚀 Открыть Rocket Keeper", 
                web_app=types.WebAppInfo(url=WEBAPP_LINK)
            )
        )
        
        await message.answer(
            f"💸 Депозит {deposit_amount} RUB подтверждён!\n"
            "Доступ к приложению:",
            reply_markup=btn
        )

    except Exception as e:
        logger.error(f"Ошибка в обработке команды /start: {e}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
