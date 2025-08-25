"""
Сервис для пагинации длинных списков рекомендаций.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.utils.logger import logger


@dataclass
class PaginationState:
    """Состояние пагинации для пользователя."""
    user_id: int
    items: List[Dict[str, Any]]
    current_page: int = 1
    items_per_page: int = 3
    category: str = "anime"
    created_at: Optional[str] = None


class PaginationService:
    """Сервис для управления пагинацией."""
    
    def __init__(self):
        """Инициализация сервиса пагинации."""
        self.pagination_states: Dict[int, PaginationState] = {}
        logger.info("PaginationService initialized")
    
    async def create_pagination(self, user_id: int, items: List[Dict[str, Any]], 
                              items_per_page: int = 3, category: str = "anime") -> PaginationState:
        """
        Создать пагинацию для пользователя.
        
        Args:
            user_id: ID пользователя
            items: Список элементов для пагинации
            items_per_page: Количество элементов на странице
            category: Категория элементов
            
        Returns:
            Состояние пагинации
        """
        pagination_state = PaginationState(
            user_id=user_id,
            items=items,
            current_page=1,
            items_per_page=items_per_page,
            category=category
        )
        
        self.pagination_states[user_id] = pagination_state
        logger.info(f"Created pagination for user {user_id}: {len(items)} items, {items_per_page} per page")
        
        return pagination_state
    
    async def get_page(self, user_id: int, page: int = None) -> Optional[Dict[str, Any]]:
        """
        Получить страницу с элементами.
        
        Args:
            user_id: ID пользователя
            page: Номер страницы (если None, возвращает текущую)
            
        Returns:
            Словарь с данными страницы или None
        """
        if user_id not in self.pagination_states:
            return None
        
        state = self.pagination_states[user_id]
        
        if page is not None:
            state.current_page = page
        
        total_items = len(state.items)
        total_pages = (total_items + state.items_per_page - 1) // state.items_per_page
        
        if state.current_page < 1:
            state.current_page = 1
        elif state.current_page > total_pages:
            state.current_page = total_pages
        
        start_idx = (state.current_page - 1) * state.items_per_page
        end_idx = start_idx + state.items_per_page
        
        page_items = state.items[start_idx:end_idx]
        
        return {
            "items": page_items,
            "current_page": state.current_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "category": state.category
        }
    
    async def get_pagination_keyboard(self, user_id: int) -> Optional[InlineKeyboardMarkup]:
        """
        Получить клавиатуру пагинации.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Клавиатура с кнопками пагинации или None
        """
        if user_id not in self.pagination_states:
            return None
        
        state = self.pagination_states[user_id]
        total_pages = (len(state.items) + state.items_per_page - 1) // state.items_per_page
        
        if total_pages <= 1:
            return None
        
        keyboard = []
        
        # Кнопки навигации
        nav_buttons = []
        
        # Кнопка "Предыдущая"
        if state.current_page > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Предыдущая", 
                    callback_data=f"page_{state.current_page - 1}"
                )
            )
        
        # Информация о странице
        nav_buttons.append(
            InlineKeyboardButton(
                text=f"{state.current_page}/{total_pages}", 
                callback_data="page_info"
            )
        )
        
        # Кнопка "Следующая"
        if state.current_page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="Следующая ➡️", 
                    callback_data=f"page_{state.current_page + 1}"
                )
            )
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Кнопка "Закрыть"
        keyboard.append([
            InlineKeyboardButton(
                text="❌ Закрыть", 
                callback_data="close_pagination"
            )
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def has_pagination(self, user_id: int) -> bool:
        """
        Проверить, есть ли пагинация у пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True, если есть пагинация
        """
        return user_id in self.pagination_states
    
    async def clear_pagination(self, user_id: int):
        """
        Очистить пагинацию пользователя.
        
        Args:
            user_id: ID пользователя
        """
        if user_id in self.pagination_states:
            del self.pagination_states[user_id]
            logger.info(f"Cleared pagination for user {user_id}")
    
    async def get_total_pages(self, user_id: int) -> int:
        """
        Получить общее количество страниц.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Количество страниц
        """
        if user_id not in self.pagination_states:
            return 0
        
        state = self.pagination_states[user_id]
        return (len(state.items) + state.items_per_page - 1) // state.items_per_page


# Глобальный экземпляр сервиса
pagination_service = PaginationService()
