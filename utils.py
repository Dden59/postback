import asyncio
import logging

logger = logging.getLogger(__name__)

async def wait_for_event(bot, channel_id: int, user_id: int, event_type: str, timeout: int = 300):
    """
    Новая версия с:
    - Поддержкой get_chat_history
    - Подробным логированием
    """
    try:
        target = str(user_id) if event_type == "Lead" else f"{user_id}|Firstdep"
        
        for _ in range(timeout // 3):
            async for msg in bot.get_chat_history(chat_id=channel_id, limit=50):
                if not msg.text:
                    continue
                    
                if event_type == "Lead" and msg.text.strip() == str(user_id):
                    logger.info(f"Найдена регистрация: {user_id}")
                    return True
                    
                if event_type == "Firstdep" and msg.text.startswith(f"{user_id}|Firstdep|"):
                    try:
                        return float(msg.text.split('|')[2])
                    except (ValueError, IndexError):
                        continue
            
            await asyncio.sleep(3)
            
        return False

    except Exception as e:
        logger.error(f"Ошибка проверки канала: {e}")
        return False
