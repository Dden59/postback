import asyncio
import logging
from aiogram import types

logger = logging.getLogger(__name__)

async def wait_for_event(bot, user_id: int, event_type: str, timeout: int = 300):
    try:
        target = str(user_id) if event_type == "Lead" else f"{user_id}|Firstdep"
        
        for _ in range(timeout // 3):
            async for message in bot.get_updates(limit=50):
                if not message.message or not message.message.text:
                    continue
                    
                text = message.message.text
                
                if event_type == "Lead" and text.strip() == str(user_id):
                    logger.info(f"Найдена регистрация: {user_id}")
                    return True
                    
                if event_type == "Firstdep" and text.startswith(f"{user_id}|Firstdep|"):
                    try:
                        return float(text.split('|')[2])
                    except (ValueError, IndexError):
                        continue
            
            await asyncio.sleep(3)
            
        return False

    except Exception as e:
        logger.error(f"Ошибка проверки: {e}")
        return False
