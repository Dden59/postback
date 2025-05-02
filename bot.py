import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, PARTNER_LINK, WEBAPP_LINK, CHANNEL_ID
from utils import wait_for_event

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    def get_keyboards(user_id: int):
        return {
            "reg": types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    "🔹 Зарегистрироваться", 
                    url=f"{PARTNER_LINK}{user_id}"
                )
            ),
            "deposit": types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    "💰 Сделать депозит", 
                    url=f"{PARTNER_LINK}{user_id}"
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
    async def start(message: types.Message):
        user_id = message.from_user.id
        kb = get_keyboards(user_id)
        
        try:
            await message.answer(
                "📝 Для доступа нужно:\n1. Зарегистрироваться\n2. Депозит от 500 RUB",
                reply_markup=kb["reg"]
            )
            
            if await wait_for_event(bot, user_id, "Lead"):
                await message.answer(
                    "✅ Регистрация подтверждена!\nПополните счет:",
                    reply_markup=kb["deposit"]
                )
                
                amount = await wait_for_event(bot, user_id, "Firstdep")
                if amount and amount >= 500:
                    await message.answer(
                        f"🎉 Депозит {amount} RUB принят!",
                        reply_markup=kb["app"]
                    )
                else:
                    await message.answer("❌ Нужен депозит от 500 RUB")
            else:
                await message.answer("⌛ Регистрация не найдена")

        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await message.answer("⚠️ Ошибка системы")

    await dp.skip_updates()
    await dp.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
