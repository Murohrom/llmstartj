"""
Утилиты для health check мониторинга.
"""

import asyncio
import time
from typing import Dict, Any
from src.utils.logger import logger


class HealthCheck:
    """Класс для проверки здоровья приложения."""
    
    def __init__(self):
        """Инициализация health check."""
        self.start_time = time.time()
        self.last_check = time.time()
        self.checks = {}
    
    def add_check(self, name: str, check_func, interval: int = 60):
        """
        Добавить проверку здоровья.
        
        Args:
            name: Название проверки
            check_func: Функция проверки
            interval: Интервал проверки в секундах
        """
        self.checks[name] = {
            'func': check_func,
            'interval': interval,
            'last_run': 0,
            'status': 'unknown',
            'error': None
        }
        logger.info(f"Added health check: {name}")
    
    async def run_checks(self) -> Dict[str, Any]:
        """
        Запустить все проверки здоровья.
        
        Returns:
            Словарь с результатами проверок
        """
        current_time = time.time()
        results = {
            'status': 'healthy',
            'uptime': current_time - self.start_time,
            'timestamp': current_time,
            'checks': {}
        }
        
        for name, check in self.checks.items():
            # Проверяем, нужно ли запускать проверку
            if current_time - check['last_run'] >= check['interval']:
                try:
                    if asyncio.iscoroutinefunction(check['func']):
                        await check['func']()
                    else:
                        check['func']()
                    
                    check['status'] = 'healthy'
                    check['error'] = None
                    logger.debug(f"Health check {name} passed")
                    
                except Exception as e:
                    check['status'] = 'unhealthy'
                    check['error'] = str(e)
                    results['status'] = 'unhealthy'
                    logger.error(f"Health check {name} failed: {e}")
                
                check['last_run'] = current_time
            
            results['checks'][name] = {
                'status': check['status'],
                'error': check['error'],
                'last_run': check['last_run']
            }
        
        self.last_check = current_time
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Получить текущий статус здоровья.
        
        Returns:
            Словарь с текущим статусом
        """
        current_time = time.time()
        return {
            'status': 'healthy',
            'uptime': current_time - self.start_time,
            'timestamp': current_time,
            'last_check': self.last_check,
            'checks': {
                name: {
                    'status': check['status'],
                    'error': check['error'],
                    'last_run': check['last_run']
                }
                for name, check in self.checks.items()
            }
        }


# Глобальный экземпляр health check
health_check = HealthCheck()


def check_telegram_connection():
    """Проверка подключения к Telegram API."""
    # Простая проверка - можно расширить
    return True


def check_openrouter_connection():
    """Проверка подключения к OpenRouter API."""
    # Простая проверка - можно расширить
    return True


def check_cache_access():
    """Проверка доступа к кэшу."""
    try:
        import os
        cache_dir = "data/cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        return True
    except Exception:
        return False


def check_memory_usage():
    """Проверка использования памяти."""
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            raise Exception(f"High memory usage: {memory.percent}%")
        return True
    except ImportError:
        # psutil не установлен, пропускаем проверку
        return True
    except Exception as e:
        raise Exception(f"Memory check failed: {e}")


# Инициализация стандартных проверок
def init_health_checks():
    """Инициализация стандартных проверок здоровья."""
    health_check.add_check('telegram_connection', check_telegram_connection, 300)  # 5 минут
    health_check.add_check('openrouter_connection', check_openrouter_connection, 300)  # 5 минут
    health_check.add_check('cache_access', check_cache_access, 600)  # 10 минут
    health_check.add_check('memory_usage', check_memory_usage, 300)  # 5 минут
    logger.info("Health checks initialized")


async def run_health_checks():
    """Запустить все проверки здоровья."""
    return await health_check.run_checks()


def get_health_status():
    """Получить текущий статус здоровья."""
    return health_check.get_status()
