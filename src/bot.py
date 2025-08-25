"""
Главный файл Telegram бота - точка входа приложения.
"""

import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError

from src.utils.config import config
from src.utils.logger import logger
from src.handlers.start import router as start_router
from src.handlers.anime import router as anime_router
from src.services.pagination_service import pagination_service


async def main():
    """Главная функция приложения."""
    try:
        # Валидируем конфигурацию
        config.validate()
        logger.info("Конфигурация валидна")
        
        # Создаем бота и диспетчер
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        
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
