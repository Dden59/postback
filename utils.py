import asyncio
from aiogram import Bot
from config import CHANNEL_ID

async def wait_for_event(bot: Bot, user_id: int, event_type: str, timeout: int = 300):
    """
    Ожидает постбэк от 1Win в формате:
    - Для регистрации: {user_id}|Lead
    - Для депозита: {user_id}|Firstdep|{amount}
    Возвращает:
    - Для Lead: True/False
    - Для Firstdep: сумму депозита или False
    """
    user_event = f"{user_id}|{event_type}"
    
    for _ in range(timeout // 3):  # Проверяем каждые 3 секунды
        try:
            async for msg in bot.get_chat_history(chat_id=CHANNEL_ID, limit=50):
                if msg.text and user_event in msg.text:
                    if event_type == "Firstdep":
                        try:
                            amount = float(msg.text.split('|')[2])
                            return amount
                        except (IndexError, ValueError):
                            continue
                    return True
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Ошибка при проверке сообщений: {e}")
            await asyncio.sleep(3)
    
    return False
