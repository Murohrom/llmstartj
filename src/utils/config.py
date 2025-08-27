"""
Конфигурация приложения через переменные окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Config:
    """Конфигурация приложения."""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # OpenRouter API
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    
    # Cache
    CACHE_TTL_HOURS: int = int(os.getenv("CACHE_TTL_HOURS", "24"))
    CACHE_DIR: str = os.getenv("CACHE_DIR", "data/cache")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "1"))
    
    @classmethod
    def validate(cls) -> None:
        """Проверяет обязательные переменные окружения."""
        required_vars = [
            ("TELEGRAM_BOT_TOKEN", cls.TELEGRAM_BOT_TOKEN),
            ("OPENROUTER_API_KEY", cls.OPENROUTER_API_KEY),
        ]
        
        missing_vars = []
        for name, value in required_vars:
            if not value or value == "your_telegram_bot_token_here" or value == "your_openrouter_api_key_here":
                missing_vars.append(name)
        
        if missing_vars:
            raise ValueError(f"Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}")


# Глобальный экземпляр конфигурации
config = Config()
