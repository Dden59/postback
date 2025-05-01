import asyncio
from aiogram import Bot
from config import CHANNEL_ID

# Проверка постбэков по user_id
async def wait_for_event(bot: Bot, user_id: int, event_type: str, timeout: int = 300):
    user_event = f"{user_id}|{event_type}"
    for _ in range(timeout):
        messages = await bot.get_chat_history(CHANNEL_ID, limit=30)
        for msg in messages:
            if user_event in msg.text:
                return True
        await asyncio.sleep(3)
    return False
