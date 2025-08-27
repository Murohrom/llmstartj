#!/usr/bin/env python3
"""Скрипт для проверки структуры данных"""

import json
from pathlib import Path


def check_data_structure():
    """Проверяет структуру данных"""
    print("Проверка структуры данных...")
    
    # Проверяем папку data
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ Папка data не найдена")
        return False
    
    print("✅ Папка data найдена")
    
    # Проверяем папку cache
    cache_dir = data_dir / "cache"
    if not cache_dir.exists():
        print("❌ Папка data/cache не найдена")
        return False
    
    print("✅ Папка data/cache найдена")
    
    # Проверяем файл кэша
    cache_file = cache_dir / "llm_cache.json"
    if not cache_file.exists():
        print("❌ Файл llm_cache.json не найден")
        return False
    
    print("✅ Файл llm_cache.json найден")
    
    # Проверяем содержимое кэша
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        print(f"✅ Кэш содержит {len(cache_data)} записей")
        return True
    except json.JSONDecodeError:
        print("❌ Файл кэша поврежден")
        return False
    except Exception as e:
        print(f"❌ Ошибка чтения кэша: {e}")
        return False


if __name__ == "__main__":
    success = check_data_structure()
    if success:
        print("\n🎉 Структура данных в порядке!")
    else:
        print("\n💥 Проблемы со структурой данных!")
