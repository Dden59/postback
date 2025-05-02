import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, CHANNEL_ID, PARTNER_LINK, WEBAPP_LINK

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

def get_keyboard(user_id: int):
    """Генератор клавиатур с защитой от подделки sub1"""
    encoded_id = str(user_id)  # Можно добавить хеширование при необходимости
    return {
        "reg": types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "🔹 Зарегистрироваться", 
                url=f"{PARTNER_LINK}?sub1={encoded_id}"
            )
        ),
        "app": types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                "🚀 Открыть приложение", 
                web_app=types.WebAppInfo(url=WEBAPP_LINK)
            )
        )
    }

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    try:
        user = message.from_user
        kb = get_keyboard(user.id)
        
        # Проверка подписки на канал
        try:
            chat_member = await bot.get_chat_member(CHANNEL_ID, user.id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                await message.answer("❌ Подпишитесь на канал для доступа!")
                return
        except Exception as e:
            logger.error(f"Ошибка проверки канала: {e}")

        await message.answer(
            "📝 Для доступа нужно:\n1. Пройти регистрацию\n2. Внести депозит от 500 RUB",
            reply_markup=kb["reg"]
        )

    except Exception as e:
        logger.critical(f"Ошибка в /start: {e}")
        await message.answer("⚠️ Системная ошибка. Попробуйте позже.")

@dp.channel_post_handler(chat_id=CHANNEL_ID)
async def handle_1win_postback(message: types.Message):
    """Обработчик постбеков из 1win"""
    try:
        text = (message.text or message.caption or "").strip()
        
        # Формат: "12345|Firstdep|500"
        if "|Firstdep|" in text:
            user_id, _, amount = text.split('|')
            amount = float(amount)
            
            if amount >= 500:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"🎉 Депозит {amount} RUB принят!",
                    reply_markup=get_keyboard(int(user_id))["app"]
                )
            else:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"❌ Требуется депозит от 500 RUB (вы внесли {amount})"
                )
                
    except Exception as e:
        logger.error(f"Ошибка обработки постбека: {e}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
