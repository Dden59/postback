import asyncio
import logging
from aiogram.types import Message

logger = logging.getLogger(__name__)

async def wait_for_event(bot, user_id: int, event_type: str, timeout: int = 300):
    """
    Улучшенная версия с:
    - Поддержкой новых методов aiogram
    - Подробным логированием
    """
    try:
        target = str(user_id) if event_type == "Lead" else f"{user_id}|Firstdep"
        
        for _ in range(timeout // 3):
            # Получаем последние сообщения через API
            messages = await bot.get_updates(limit=50)
            
            for update in messages:
                if not update.message or not update.message.text:
                    continue
                    
                msg = update.message.text
                
                if event_type == "Lead" and msg.strip() == str(user_id):
                    logger.info(f"Найдена регистрация: {user_id}")
                    return True
                    
                if event_type == "Firstdep" and msg.startswith(f"{user_id}|Firstdep|"):
                    try:
                        return float(msg.split('|')[2])
                    except (ValueError, IndexError):
                        continue
            
            await asyncio.sleep(3)
            
        return False

    except Exception as e:
        logger.error(f"Ошибка проверки: {e}")
        return False
