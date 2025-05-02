import logging
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN, CHANNEL_ID, PARTNER_LINK, WEBAPP_LINK

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def create_keyboard(user_id: int):
    """Генерация кнопок с защищенным sub1"""
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "🚀 Открыть приложение",
            web_app=types.WebAppInfo(url=WEBAPP_LINK)
        )
    )

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    await message.answer(
        f"👋 Добро пожаловать, {user.first_name}!\n"
        "После регистрации и депозита от 500 RUB вы получите доступ к приложению.",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "🔹 Зарегистрироваться",
                url=f"{PARTNER_LINK}{user.id}"
            )
        )
    )

@dp.channel_post_handler(chat_id=CHANNEL_ID)
async def handle_1win_postback(message: types.Message):
    """Обработчик постбеков из канала"""
    try:
        text = message.text.strip()
        
        # Формат: "12345|Firstdep|500"
        if "|Firstdep|" in text:
            user_id, _, amount = text.split('|')
            amount = float(amount)
            
            if amount >= 500:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"🎉 Депозит {amount} RUB принят!",
                    reply_markup=create_keyboard(int(user_id))
                )
                logger.info(f"Доступ выдан для {user_id}")
                
    except Exception as e:
        logger.error(f"Ошибка обработки постбека: {e}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
