"""
Сервис для работы с OpenRouter API и генерации ответов LLM.
"""

import asyncio
import logging
from typing import List, Dict, Any
from openai import AsyncOpenAI
from openai import APIError, RateLimitError, APITimeoutError

from src.utils.config import config
from src.utils.logger import logger
from src.utils.prompts import (
    SYSTEM_PROMPT, 
    TOP_ANIME_PROMPT, 
    NEW_ANIME_PROMPT, 
    CLASSIC_ANIME_PROMPT
)
from src.utils.message_utils import truncate_message, format_error_message
from src.services.cache_service import cache_service
from src.services.user_state_service import user_state_service


class LLMService:
    """Сервис для работы с LLM через OpenRouter API."""
    
    def __init__(self):
        """Инициализация клиента OpenRouter."""
        self.client = AsyncOpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = config.OPENROUTER_MODEL
        self.max_retries = config.MAX_RETRIES
        self.retry_delay = config.RETRY_DELAY
    
    async def generate_response(self, user_message: str, user_id: int) -> str:
        """
        Генерирует ответ через OpenRouter API в стиле Сайтамы с контекстом диалога.
        
        Args:
            user_message: Сообщение пользователя
            user_id: ID пользователя для логирования и контекста
            
        Returns:
            Ответ от LLM в стиле Сайтамы
        """
        try:
            logger.info(f"LLM request for user {user_id}: {user_message}")
            
            # Получаем контекст диалога
            conversation_context = await user_state_service.get_conversation_context(user_id)
            
            # Добавляем новое сообщение пользователя в историю
            await user_state_service.add_message_to_history(user_id, "user", user_message)
            
            # Формируем промпт с контекстом
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Добавляем контекст диалога
            if conversation_context:
                messages.extend(conversation_context)
                logger.info(f"Using conversation context for user {user_id}: {len(conversation_context)} messages")
            
            # Добавляем текущее сообщение пользователя
            messages.append({"role": "user", "content": user_message})
            
            # Проверяем кэш только для одиночных сообщений без контекста
            if not conversation_context:
                cached_response = await cache_service.get_cached_response(user_message)
                if cached_response:
                    logger.info(f"Returning cached response for user {user_id}")
                    # Добавляем кэшированный ответ в историю
                    await user_state_service.add_message_to_history(user_id, "assistant", cached_response)
                    return cached_response
            
            # Запрашиваем API
            response = await self._make_api_request(messages)
            
            # Обрезаем ответ до максимальной длины
            response = truncate_message(response)
            
            # Добавляем ответ в историю диалога
            await user_state_service.add_message_to_history(user_id, "assistant", response)
            
            # Сохраняем в кэш только одиночные сообщения
            if not conversation_context:
                await cache_service.save_response(user_message, response, self.model)
            
            logger.info(f"LLM response for user {user_id}: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response for user {user_id}: {e}")
            return self._get_error_response()
    
    async def _make_api_request(self, messages: List[Dict[str, str]]) -> str:
        """
        Отправляет запрос к OpenRouter API с retry логикой.
        
        Args:
            messages: Список сообщений для API
            
        Returns:
            Ответ от LLM
            
        Raises:
            Exception: При неудачных попытках
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                    timeout=30
                )
                
                return response.choices[0].message.content.strip()
                
            except RateLimitError as e:
                last_error = e
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}")
                await asyncio.sleep(wait_time)
                
            except APITimeoutError as e:
                last_error = e
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"API timeout, waiting {wait_time}s before retry {attempt + 1}")
                await asyncio.sleep(wait_time)
                
            except APIError as e:
                last_error = e
                logger.error(f"API error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.retry_delay)
                
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                raise
        
        # Если все попытки исчерпаны
        raise last_error or Exception("All retry attempts failed")
    

    
    def _get_error_response(self, error_type: str = "general") -> str:
        """Возвращает сообщение об ошибке в стиле Сайтамы."""
        return format_error_message(error_type)
    
    async def generate_category_response(self, category: str, user_id: int) -> str:
        """
        Генерирует ответ для конкретной категории аниме.
        
        Args:
            category: Категория (top, new, classic)
            user_id: ID пользователя для логирования
            
        Returns:
            Ответ от LLM для категории
        """
        try:
            logger.info(f"Category request for user {user_id}: {category}")
            
            # Выбираем промпт в зависимости от категории
            if category == "top":
                system_prompt = TOP_ANIME_PROMPT
                user_message = "Покажи популярные аниме"
            elif category == "new":
                system_prompt = NEW_ANIME_PROMPT
                user_message = "Покажи новинки сезона"
            elif category == "classic":
                system_prompt = CLASSIC_ANIME_PROMPT
                user_message = "Покажи классические аниме"
            else:
                return "Хм... Не знаю такую категорию."
            
            # Формируем промпт
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Запрашиваем API
            response = await self._make_api_request(messages)
            
            # Обрезаем ответ до максимальной длины
            response = truncate_message(response)
            
            # Добавляем в историю диалога
            await user_state_service.add_message_to_history(user_id, "user", f"/{category}")
            await user_state_service.add_message_to_history(user_id, "assistant", response)
            
            logger.info(f"Category response for user {user_id}: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating category response for user {user_id}: {e}")
            return self._get_error_response()


# Глобальный экземпляр сервиса
llm_service = LLMService()
