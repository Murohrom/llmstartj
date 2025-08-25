"""
Утилиты для работы с сообщениями Telegram.
"""

from typing import List, Dict, Any

# Максимальная длина сообщения Telegram
MAX_MESSAGE_LENGTH = 4096


def truncate_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> str:
    """
    Обрезать сообщение до максимальной длины, сохраняя целостность предложений.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина сообщения
        
    Returns:
        Обрезанный текст с многоточием
    """
    if len(text) <= max_length:
        return text
    
    # Обрезаем до последнего полного предложения
    truncated = text[:max_length-3] + "..."
    last_sentence_end = truncated.rfind('.')
    
    # Если есть место для полного предложения (80% от лимита)
    if last_sentence_end > max_length * 0.8:
        return truncated[:last_sentence_end+1] + "..."
    
    return truncated


def format_anime_list(anime_items: List[Dict[str, Any]], category: str = "anime") -> str:
    """
    Форматировать список аниме в красивом виде.
    
    Args:
        anime_items: Список аниме с информацией
        category: Категория аниме (top, new, classic)
        
    Returns:
        Отформатированный текст
    """
    if not anime_items:
        return "Хм... Ничего не нашел."
    
    # Эмодзи для категорий
    category_emojis = {
        "top": "🔥",
        "new": "🆕", 
        "classic": "👑",
        "anime": "📺"
    }
    
    emoji = category_emojis.get(category, "📺")
    
    # Формируем заголовок
    result = f"{emoji} Рекомендации:\n\n"
    
    for i, item in enumerate(anime_items, 1):
        title = item.get("title", "Неизвестное аниме")
        year = item.get("year", "")
        rating = item.get("rating", "")
        description = item.get("description", "")
        
        # Форматируем каждое аниме
        anime_line = f"{i}. 🏆 {title}"
        if year:
            anime_line += f" ({year})"
        anime_line += "\n"
        
        if rating:
            anime_line += f"   ⭐ {rating}\n"
        
        if description:
            anime_line += f"   📝 {description}\n"
        
        anime_line += "\n"
        result += anime_line
    
    return result


def split_long_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """
    Разбить длинное сообщение на части.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина части
        
    Returns:
        Список частей сообщения
    """
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    
    # Разбиваем по строкам
    lines = text.split('\n')
    
    for line in lines:
        # Если текущая часть + новая строка превышает лимит
        if len(current_part) + len(line) + 1 > max_length:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""
            
            # Если одна строка слишком длинная, разбиваем её
            if len(line) > max_length:
                while len(line) > max_length:
                    parts.append(line[:max_length])
                    line = line[max_length:]
                current_part = line
            else:
                current_part = line
        else:
            if current_part:
                current_part += '\n' + line
            else:
                current_part = line
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts


def create_pagination_info(current_page: int, total_pages: int, total_items: int) -> str:
    """
    Создать информацию о пагинации.
    
    Args:
        current_page: Текущая страница
        total_pages: Общее количество страниц
        total_items: Общее количество элементов
        
    Returns:
        Строка с информацией о пагинации
    """
    if total_pages <= 1:
        return ""
    
    return f"\n📄 Страница {current_page} из {total_pages} ({total_items} аниме)"


def format_error_message(error_type: str = "general") -> str:
    """
    Форматировать сообщение об ошибке в стиле Сайтамы.
    
    Args:
        error_type: Тип ошибки
        
    Returns:
        Сообщение об ошибке
    """
    error_messages = {
        "api": "Хм... Что-то с интернетом. Попробуй еще раз.",
        "timeout": "Ладно, сервис тормозит. Подожди немного.",
        "rate_limit": "Слишком много запросов. Подожди немного.",
        "general": "Хм... Что-то пошло не так. Попробуй еще раз."
    }
    
    return error_messages.get(error_type, error_messages["general"])
