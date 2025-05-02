import asyncio
from aiogram import Bot
from config import CHANNEL_ID

async def wait_for_event(bot: Bot, user_id: int, event_type: str, timeout: int = 300):
    """
    Ожидает постбэк в указанном формате:
    - Регистрация: {user_id}
    - Депозит: {user_id}|Firstdep|{amount}
    """
    for _ in range(timeout // 5):  # Проверяем каждые 5 секунд
        try:
            async for msg in bot.get_chat_history(chat_id=CHANNEL_ID, limit=100):
                if not msg.text:
                    continue
                
                # Для регистрации
                if event_type == "Lead" and msg.text.strip() == str(user_id):
                    return True
                
                # Для депозита
                if event_type == "Firstdep":
                    parts = msg.text.split('|')
                    if len(parts) == 3 and parts[0] == str(user_id) and parts[1] == "Firstdep":
                        try:
                            return float(parts[2])  # Возвращаем сумму
                        except ValueError:
                            continue
                            
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Ошибка при проверке канала: {e}")
            await asyncio.sleep(5)
    
    return False
