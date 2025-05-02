import asyncio
import logging
from aiogram import Bot

logger = logging.getLogger(__name__)

async def wait_for_event(bot: Bot, user_id: int, event_type: str, timeout: int = 300):
    try:
        target = str(user_id) if event_type == "Lead" else f"{user_id}|Firstdep"
        
        for _ in range(timeout // 5):
            async with bot.session as session:
                updates = await bot.get_updates(limit=50, session=session)
                
                for update in updates:
                    if update.message and update.message.text:
                        text = update.message.text
                        
                        if event_type == "Lead" and text.strip() == str(user_id):
                            return True
                            
                        if event_type == "Firstdep" and text.startswith(f"{user_id}|Firstdep|"):
                            try:
                                return float(text.split('|')[2])
                            except (ValueError, IndexError):
                                continue
            
            await asyncio.sleep(5)
            
        return False

    except Exception as e:
        logger.error(f"Ошибка проверки: {e}")
        return False
