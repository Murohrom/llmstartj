"""
Обработчик текстовых сообщений для подбора аниме через LLM.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from src.services.llm_service import llm_service
from src.utils.logger import logger
from src.utils.message_utils import format_error_message

router = Router()


@router.message(F.text)
async def handle_text_message(message: Message):
    """
    Обработчик всех текстовых сообщений через LLM.
    
    Обрабатывает любые текстовые сообщения, отправляя их в LLM
    и возвращая ответ в стиле Сайтамы.
    """
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_text = message.text.strip()
    
    # Логируем входящее сообщение
    logger.info(f"User {user_id} ({user_name}) sent text: {user_text}")
    
    try:
        # Отправляем "печатает" статус
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Генерируем ответ через LLM
        response = await llm_service.generate_response(user_text, user_id)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Sent LLM response to user {user_id}")
        
    except TelegramBadRequest as e:
        logger.error(f"Telegram API error for user {user_id}: {e}")
        await message.answer(format_error_message("general"))
        
    except Exception as e:
        logger.error(f"Unexpected error for user {user_id}: {e}")
        await message.answer(format_error_message("timeout"))
