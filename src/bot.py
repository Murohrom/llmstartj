"""
Главный файл Telegram бота - точка входа приложения.
"""

import asyncio
import sys
import json
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError

from src.utils.config import config
from src.utils.logger import logger
from src.utils.health_check import init_health_checks
from src.handlers.start import router as start_router
from src.handlers.anime import router as anime_router
from src.services.pagination_service import pagination_service


async def main():
    """Главная функция приложения."""
    try:
        # Инициализируем структуру данных
        data_dir = Path("data")
        cache_dir = data_dir / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем пустой кэш если его нет
        cache_file = cache_dir / "llm_cache.json"
        if not cache_file.exists():
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            logger.info("Создан пустой файл кэша")
        
        # Валидируем конфигурацию
        config.validate()
        logger.info("Конфигурация валидна")
        
        # Создаем бота и диспетчер
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        
        # Инициализируем health checks
        init_health_checks()
        
        # Регистрируем роутеры
        dp.include_router(start_router)
        dp.include_router(anime_router)
        
        logger.info("Бот запускается...")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        sys.exit(1)
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {e}")
        sys.exit(1)
    except TelegramNetworkError as e:
        logger.error(f"Ошибка сети: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        sys.exit(1)
    finally:
        if 'bot' in locals():
            await bot.session.close()
            logger.info("Сессия бота закрыта")


if __name__ == "__main__":
    asyncio.run(main())
