import asyncio
from aiogram import types
import logging

logger = logging.getLogger(__name__)

async def wait_for_event(bot, user_id: int, event_type: str, timeout: int = 300):
    """
    Улучшенная версия с:
    - Поддержкой новых методов aiogram
    - Обработкой ошибок
    """
    try:
        # Получаем последние сообщения через клиент
        messages = await bot.client.get_messages(
            entity=-1002665040288,  # Ваш CHANNEL_ID
            limit=50
        )
        
        target = str(user_id) if event_type == "Lead" else f"{user_id}|Firstdep"
        
        for msg in messages:
            if not msg.text:
                continue
                
            if event_type == "Lead" and msg.text.strip() == str(user_id):
                logger.info(f"✅ Найдена регистрация для {user_id}")
                return True
                
            if event_type == "Firstdep" and msg.text.startswith(f"{user_id}|Firstdep|"):
                try:
                    return float(msg.text.split('|')[2])
                except (IndexError, ValueError):
                    continue
                    
        return False

    except Exception as e:
        logger.error(f"🔥 Ошибка: {str(e)}")
        return False
