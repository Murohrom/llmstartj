#!/usr/bin/env python3
"""Скрипт для проверки готовности к деплою"""

import os
from pathlib import Path


def check_deploy_readiness():
    """Проверяет готовность проекта к деплою"""
    print("🔍 Проверка готовности к деплою...")
    
    errors = []
    warnings = []
    
    # Проверяем обязательные файлы
    required_files = [
        "requirements.txt",
        "src/bot.py",
        "src/utils/config.py",
        "src/utils/logger.py",
        "src/handlers/start.py",
        "src/handlers/anime.py",
        "src/services/llm_service.py",
        "src/services/cache_service.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"❌ Файл {file_path} не найден")
        else:
            print(f"✅ {file_path}")
    
    # Проверяем Dockerfile
    dockerfiles = ["Dockerfile", "Dockerfile.railway", "Dockerfile.railway.simple"]
    dockerfile_found = False
    
    for dockerfile in dockerfiles:
        if Path(dockerfile).exists():
            print(f"✅ {dockerfile}")
            dockerfile_found = True
    
    if not dockerfile_found:
        errors.append("❌ Не найден ни один Dockerfile")
    
    # Проверяем переменные окружения
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env файл найден")
    else:
        warnings.append("⚠️  .env файл не найден (нужно создать)")
    
    # Проверяем структуру данных
    data_dir = Path("data")
    if data_dir.exists():
        print("✅ Папка data найдена")
        cache_dir = data_dir / "cache"
        if cache_dir.exists():
            print("✅ Папка data/cache найдена")
        else:
            warnings.append("⚠️  Папка data/cache не найдена (создастся автоматически)")
    else:
        warnings.append("⚠️  Папка data не найдена (создастся автоматически)")
    
    # Выводим результаты
    print("\n" + "="*50)
    
    if errors:
        print("❌ ОШИБКИ:")
        for error in errors:
            print(f"  {error}")
        print()
    
    if warnings:
        print("⚠️  ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    if not errors and not warnings:
        print("🎉 Проект готов к деплою!")
        return True
    elif not errors:
        print("✅ Проект готов к деплою (есть предупреждения)")
        return True
    else:
        print("💥 Проект не готов к деплою")
        return False


if __name__ == "__main__":
    check_deploy_readiness()
