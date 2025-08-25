"""
Сервис кэширования ответов LLM для экономии API-вызовов.
"""

import json
import hashlib
import time
import os
from typing import Optional, Dict, Any
from pathlib import Path

from src.utils.config import config
from src.utils.logger import logger


class CacheService:
    """Сервис для кэширования ответов LLM."""
    
    def __init__(self):
        """Инициализация сервиса кэширования."""
        self.cache_dir = Path(config.CACHE_DIR)
        self.cache_file = self.cache_dir / "llm_cache.json"
        self.ttl_hours = config.CACHE_TTL_HOURS
        
        # Создаем папку кэша, если не существует
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Загружаем существующий кэш
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Загружает кэш из файла."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                logger.info(f"Загружен кэш из {self.cache_file}")
            else:
                self.cache = {}
                logger.info("Создан новый кэш")
        except Exception as e:
            logger.error(f"Ошибка загрузки кэша: {e}")
            self.cache = {}
    
    def _save_cache(self) -> None:
        """Сохраняет кэш в файл."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logger.debug(f"Кэш сохранен в {self.cache_file}")
        except Exception as e:
            logger.error(f"Ошибка сохранения кэша: {e}")
    
    def _generate_hash(self, query: str) -> str:
        """
        Генерирует MD5 хэш от нормализованного запроса.
        
        Args:
            query: Запрос пользователя
            
        Returns:
            MD5 хэш запроса
        """
        # Нормализуем запрос: убираем лишние пробелы, приводим к нижнему регистру
        normalized_query = query.strip().lower()
        return hashlib.md5(normalized_query.encode('utf-8')).hexdigest()
    
    def _is_expired(self, timestamp: int) -> bool:
        """
        Проверяет, истек ли TTL кэша.
        
        Args:
            timestamp: Временная метка создания записи
            
        Returns:
            True если запись истекла
        """
        current_time = int(time.time())
        ttl_seconds = self.ttl_hours * 3600
        return (current_time - timestamp) > ttl_seconds
    
    async def get_cached_response(self, query: str) -> Optional[str]:
        """
        Получает ответ из кэша по запросу.
        
        Args:
            query: Запрос пользователя
            
        Returns:
            Ответ из кэша или None, если не найден или истек
        """
        query_hash = self._generate_hash(query)
        
        if query_hash in self.cache:
            cache_entry = self.cache[query_hash]
            
            # Проверяем TTL
            if self._is_expired(cache_entry['timestamp']):
                logger.info(f"Запись кэша истекла для запроса: {query[:50]}...")
                del self.cache[query_hash]
                self._save_cache()
                return None
            
            logger.info(f"Найден ответ в кэше для запроса: {query[:50]}...")
            return cache_entry['response']
        
        return None
    
    async def save_response(self, query: str, response: str, model: str) -> None:
        """
        Сохраняет ответ в кэш.
        
        Args:
            query: Запрос пользователя
            response: Ответ LLM
            model: Модель LLM
        """
        query_hash = self._generate_hash(query)
        current_time = int(time.time())
        
        cache_entry = {
            'query': query,
            'response': response,
            'timestamp': current_time,
            'model': model
        }
        
        self.cache[query_hash] = cache_entry
        self._save_cache()
        
        logger.info(f"Ответ сохранен в кэш для запроса: {query[:50]}...")
    
    async def clear_expired(self) -> int:
        """
        Очищает истекшие записи из кэша.
        
        Returns:
            Количество удаленных записей
        """
        expired_keys = []
        
        for key, entry in self.cache.items():
            if self._is_expired(entry['timestamp']):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
            logger.info(f"Удалено {len(expired_keys)} истекших записей из кэша")
        
        return len(expired_keys)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику кэша.
        
        Returns:
            Словарь со статистикой
        """
        total_entries = len(self.cache)
        expired_entries = sum(1 for entry in self.cache.values() 
                            if self._is_expired(entry['timestamp']))
        
        return {
            'total_entries': total_entries,
            'expired_entries': expired_entries,
            'valid_entries': total_entries - expired_entries,
            'cache_file_size': self.cache_file.stat().st_size if self.cache_file.exists() else 0
        }


# Глобальный экземпляр сервиса кэширования
cache_service = CacheService()
