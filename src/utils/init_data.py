"""Скрипт для инициализации структуры данных"""
import os
import json
from pathlib import Path


def init_data_structure():
    """Создает структуру данных если она не существует"""
    data_dir = Path("data")
    cache_dir = data_dir / "cache"
    
    # Создаем папки если их нет
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Создаем пустой кэш если его нет
    cache_file = cache_dir / "llm_cache.json"
    if not cache_file.exists():
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        print("Создан пустой файл кэша")


if __name__ == "__main__":
    init_data_structure()
