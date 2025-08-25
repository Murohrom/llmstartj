"""
Обработчики команд /start и /help.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.utils.logger import logger
from src.services.user_state_service import user_state_service

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /start command")
    
    welcome_text = (
        f"Ладно... Привет, {user_name}.\n\n"
        "Я Сайтама, и теперь помогаю подбирать аниме. "
        "Не самая захватывающая работа, но ладно...\n\n"
        "Расскажи мне, что хочешь посмотреть, и я найду что-нибудь подходящее.\n\n"
        "Используй /help для справки."
    )
    
    await message.answer(welcome_text)
    logger.info(f"Sent welcome message to user {user_id}")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /help command")
    
    help_text = (
        "Хм... Вот что я умею:\n\n"
        "📋 <b>Команды:</b>\n"
        "• /start - начать общение\n"
        "• /help - показать эту справку\n"
        "• /reset - забыть историю разговора\n\n"
        "💬 <b>Как использовать:</b>\n"
        "Просто напиши мне, какое аниме ищешь или что тебе нравится. "
        "Я помню наш разговор и порекомендую что-то подходящее.\n\n"
        "Например:\n"
        "• \"Хочу что-то с драками\"\n"
        "• \"Ищу романтическое аниме\"\n"
        "• \"Покажи что-то смешное\"\n\n"
        "Ладно, попробуй что-нибудь написать."
    )
    
    await message.answer(help_text, parse_mode="HTML")
    logger.info(f"Sent help message to user {user_id}")


@router.message(Command("reset"))
async def cmd_reset(message: Message):
    """Обработчик команды /reset - сброс состояния пользователя."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /reset command")
    
    # Сбрасываем состояние пользователя
    await user_state_service.reset_user_state(user_id)
    
    reset_text = (
        "Окей, забыл что ты хотел. Начнем заново.\n\n"
        "Расскажи мне, что хочешь посмотреть."
    )
    
    await message.answer(reset_text)
    logger.info(f"Reset user state for user {user_id}")
