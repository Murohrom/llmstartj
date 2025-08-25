"""
Сервис для управления состояниями пользователей и историей диалогов.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from src.utils.logger import logger


@dataclass
class UserState:
    """Состояние пользователя в диалоге."""
    user_id: int
    state: str = "idle"  # idle, waiting_preferences, etc.
    preferences: Dict = field(default_factory=dict)
    conversation_history: List[Dict] = field(default_factory=list)
    last_query: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class UserStateService:
    """Сервис для управления состояниями пользователей."""
    
    def __init__(self):
        """Инициализация сервиса состояний."""
        self.user_states: Dict[int, UserState] = {}
        logger.info("UserStateService initialized")
    
    async def get_user_state(self, user_id: int) -> UserState:
        """
        Получить состояние пользователя, создавая новое если не существует.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Объект состояния пользователя
        """
        if user_id not in self.user_states:
            self.user_states[user_id] = UserState(user_id=user_id)
            logger.info(f"Created new user state for user {user_id}")
        
        return self.user_states[user_id]
    
    async def add_message_to_history(self, user_id: int, role: str, content: str):
        """
        Добавить сообщение в историю диалога пользователя.
        
        Args:
            user_id: ID пользователя
            role: Роль сообщения (user/assistant)
            content: Содержимое сообщения
        """
        user_state = await self.get_user_state(user_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        
        user_state.conversation_history.append(message)
        user_state.updated_at = datetime.now()
        
        logger.info(f"Added {role} message to history for user {user_id}")
    
    async def get_conversation_context(self, user_id: int, max_tokens: int = 3000) -> List[Dict]:
        """
        Получить контекст диалога с ограничением по токенам.
        
        Args:
            user_id: ID пользователя
            max_tokens: Максимальное количество токенов для контекста
            
        Returns:
            Список сообщений для контекста LLM
        """
        user_state = await self.get_user_state(user_id)
        
        if not user_state.conversation_history:
            return []
        
        # Простая эвристика: примерно 4 символа = 1 токен
        # Берем последние сообщения, которые помещаются в лимит
        context = []
        total_chars = 0
        
        # Идем с конца истории (новые сообщения)
        for message in reversed(user_state.conversation_history):
            message_chars = len(message["content"])
            
            if total_chars + message_chars > max_tokens * 4:
                break
                
            context.insert(0, {
                "role": message["role"],
                "content": message["content"]
            })
            total_chars += message_chars
        
        logger.info(f"Generated context for user {user_id}: {len(context)} messages, ~{total_chars} chars")
        return context
    
    async def reset_user_state(self, user_id: int):
        """
        Сбросить состояние пользователя (очистить историю).
        
        Args:
            user_id: ID пользователя
        """
        if user_id in self.user_states:
            old_history_length = len(self.user_states[user_id].conversation_history)
            self.user_states[user_id] = UserState(user_id=user_id)
            logger.info(f"Reset user state for user {user_id}, cleared {old_history_length} messages")
        else:
            logger.info(f"User {user_id} had no state to reset")
    
    async def get_user_stats(self, user_id: int) -> Dict:
        """
        Получить статистику пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Словарь со статистикой
        """
        user_state = await self.get_user_state(user_id)
        
        return {
            "user_id": user_id,
            "messages_count": len(user_state.conversation_history),
            "created_at": user_state.created_at,
            "last_activity": user_state.updated_at
        }


# Глобальный экземпляр сервиса
user_state_service = UserStateService()
