import asyncio
from aiogram import Bot
from config import CHANNEL_ID
import logging

logger = logging.getLogger(__name__)

async def wait_for_event(bot: Bot, user_id: int, event_type: str, timeout: int = 300):
    """
    Ищет постбэки в канале в формате:
    - Регистрация: {user_id}
    - Депозит: {user_id}|Firstdep|{amount}
    """
    try:
        # Проверка доступа к каналу
        chat = await bot.get_chat(CHANNEL_ID)
        logger.info(f"🔎 Проверяю канал: {chat.title} (ID: {chat.id})")

        for _ in range(timeout // 5):  # Проверяем каждые 5 секунд
            async for msg in bot.get_chat_history(chat_id=CHANNEL_ID, limit=50):
                if not msg.text:
                    continue
                
                # Для регистрации
                if event_type == "Lead" and msg.text.strip() == str(user_id):
                    logger.info(f"✅ Найдена регистрация для {user_id}")
                    return True
                
                # Для депозита
                if event_type == "Firstdep" and msg.text.startswith(f"{user_id}|Firstdep|"):
                    try:
                        amount = float(msg.text.split('|')[2])
                        logger.info(f"✅ Найден депозит: {amount} RUB")
                        return amount
                    except (IndexError, ValueError):
                        continue
            
            await asyncio.sleep(5)
        
        logger.warning(f"❌ Событие не найдено для {user_id}")
        return False

    except Exception as e:
        logger.error(f"🔥 Ошибка при проверке канала: {str(e)}")
        return False
