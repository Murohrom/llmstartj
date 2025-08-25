"""
Обработчики команд /start и /help.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from src.utils.logger import logger
from src.utils.message_utils import format_error_message
from src.services.user_state_service import user_state_service
from src.services.llm_service import llm_service
from src.services.pagination_service import pagination_service

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
        "• /reset - забыть историю разговора\n"
        "• /top - популярные аниме\n"
        "• /new - новинки сезона\n"
        "• /classic - классические аниме\n\n"
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


@router.message(Command("top"))
async def cmd_top(message: Message):
    """Обработчик команды /top - популярные аниме."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /top command")
    
    try:
        # Отправляем "печатает" статус
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Генерируем ответ для категории
        response = await llm_service.generate_category_response("top", user_id)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Sent top anime response to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in /top command for user {user_id}: {e}")
        await message.answer(format_error_message("api"))


@router.message(Command("new"))
async def cmd_new(message: Message):
    """Обработчик команды /new - новинки сезона."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /new command")
    
    try:
        # Отправляем "печатает" статус
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Генерируем ответ для категории
        response = await llm_service.generate_category_response("new", user_id)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Sent new anime response to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in /new command for user {user_id}: {e}")
        await message.answer(format_error_message("api"))


@router.message(Command("classic"))
async def cmd_classic(message: Message):
    """Обработчик команды /classic - классические аниме."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) sent /classic command")
    
    try:
        # Отправляем "печатает" статус
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Генерируем ответ для категории
        response = await llm_service.generate_category_response("classic", user_id)
        
        # Отправляем ответ пользователю
        await message.answer(response)
        
        logger.info(f"Sent classic anime response to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in /classic command for user {user_id}: {e}")
        await message.answer(format_error_message("api"))


def get_categories_keyboard():
    """Клавиатура с категориями аниме"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔥 Популярные", callback_data="category_top"),
            InlineKeyboardButton(text="🆕 Новинки", callback_data="category_new")
        ],
        [
            InlineKeyboardButton(text="👑 Классика", callback_data="category_classic"),
            InlineKeyboardButton(text="🎯 Персональные", callback_data="category_personal")
        ]
    ])
    return keyboard


@router.callback_query(F.data.startswith("category_"))
async def handle_category_callback(callback: CallbackQuery):
    """Обработчик нажатий на кнопки категорий."""
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    category = callback.data.replace("category_", "")
    
    logger.info(f"User {user_id} ({user_name}) clicked category: {category}")
    
    try:
        # Отвечаем на callback
        await callback.answer()
        
        # Отправляем "печатает" статус
        await callback.bot.send_chat_action(callback.message.chat.id, "typing")
        
        if category == "personal":
            # Для персональных рекомендаций используем обычный диалог
            await callback.message.answer(
                "Ладно, расскажи что тебе нравится, и я подберу что-то подходящее."
            )
        else:
            # Генерируем ответ для категории
            response = await llm_service.generate_category_response(category, user_id)
            
            # Отправляем ответ пользователю
            await callback.message.answer(response)
        
        logger.info(f"Sent category response to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in category callback for user {user_id}: {e}")
        await callback.message.answer(format_error_message("api"))


@router.callback_query(F.data.startswith("page_"))
async def handle_pagination_callback(callback: CallbackQuery):
    """Обработчик нажатий на кнопки пагинации."""
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    data = callback.data
    
    logger.info(f"User {user_id} ({user_name}) clicked pagination: {data}")
    
    try:
        # Отвечаем на callback
        await callback.answer()
        
        if data == "page_info":
            # Показать информацию о странице
            total_pages = await pagination_service.get_total_pages(user_id)
            if total_pages > 0:
                await callback.message.answer(f"📄 Всего страниц: {total_pages}")
            return
        
        if data == "close_pagination":
            # Закрыть пагинацию
            await pagination_service.clear_pagination(user_id)
            await callback.message.edit_text("Окей, закрыл список.")
            return
        
        # Получаем номер страницы
        page = int(data.replace("page_", ""))
        
        # Получаем данные страницы
        page_data = await pagination_service.get_page(user_id, page)
        if not page_data:
            await callback.message.answer("Хм... Страница не найдена.")
            return
        
        # Форматируем ответ
        items = page_data["items"]
        category = page_data["category"]
        
        # Создаем текст ответа
        response_text = f"📺 Рекомендации (страница {page_data['current_page']} из {page_data['total_pages']}):\n\n"
        
        for i, item in enumerate(items, 1):
            title = item.get("title", "Неизвестное аниме")
            year = item.get("year", "")
            rating = item.get("rating", "")
            description = item.get("description", "")
            
            response_text += f"{i}. 🏆 {title}"
            if year:
                response_text += f" ({year})"
            response_text += "\n"
            
            if rating:
                response_text += f"   ⭐ {rating}\n"
            
            if description:
                response_text += f"   📝 {description}\n"
            
            response_text += "\n"
        
        # Получаем клавиатуру пагинации
        keyboard = await pagination_service.get_pagination_keyboard(user_id)
        
        # Обновляем сообщение
        await callback.message.edit_text(response_text, reply_markup=keyboard)
        
        logger.info(f"Updated pagination for user {user_id}, page {page}")
        
    except Exception as e:
        logger.error(f"Error in pagination callback for user {user_id}: {e}")
        await callback.message.answer(format_error_message("general"))
