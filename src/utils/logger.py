"""
Настройка логирования для приложения.
"""

import logging
from src.utils.config import config


def setup_logger(name: str = "anime_bot") -> logging.Logger:
    """Настраивает и возвращает логгер."""
    logger = logging.getLogger(name)
    
    # Устанавливаем уровень логирования
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Создаем обработчик для вывода в консоль
    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Создаем форматтер
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(handler)
    
    return logger


# Глобальный логгер
logger = setup_logger()
