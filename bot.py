import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, PARTNER_LINK, WEBAPP_LINK
from utils import wait_for_event

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
users_in_progress = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    users_in_progress[user_id] = {"reg": False, "dep": False}
    link = f"{PARTNER_LINK}{user_id}"
    await message.answer(
        f"👋 Привет! Чтобы начать использовать Rocket Keeper, нужно сначала зарегистрироваться:\n\n"
        f"🔗 {link}\n\n"
        f"После регистрации я дам тебе доступ к следующему шагу..."
    )

    # Ожидаем регистрацию
    registered = await wait_for_event(bot, user_id, "Lead")
    if registered:
        users_in_progress[user_id]["reg"] = True
        await message.answer("✅ Регистрация прошла успешно! Теперь сделай депозит...")

        # Ожидаем депозит
        deposited = await wait_for_event(bot, user_id, "Firstdep")
        if deposited:
            users_in_progress[user_id]["dep"] = True
            btn = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🚀 Открыть Rocket Keeper", web_app=types.WebAppInfo(url=WEBAPP_LINK))
            )
            await message.answer("💸 Депозит получен! Можешь пользоваться приложением:", reply_markup=btn)
        else:
            await message.answer("❌ Время ожидания депозита истекло.")
    else:
        await message.answer("❌ Время ожидания регистрации истекло.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
