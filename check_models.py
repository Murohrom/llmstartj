#!/usr/bin/env python3
"""Скрипт для проверки доступности моделей OpenRouter"""

import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


async def check_models():
    """Проверяет доступность моделей OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в переменных окружения")
        return
    
    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Список моделей для проверки
    models_to_check = [
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3-haiku", 
        "google/gemini-pro",
        "meta-llama/llama-3.1-8b-instruct:free"
    ]
    
    print("🔍 Проверка доступности моделей OpenRouter...")
    print("=" * 50)
    
    available_models = []
    
    for model in models_to_check:
        try:
            print(f"Проверяю {model}...", end=" ")
            
            # Пробуем отправить простой запрос
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Привет"}],
                max_tokens=10,
                timeout=10
            )
            
            print("✅ Доступна")
            available_models.append(model)
            
        except Exception as e:
            print(f"❌ Недоступна: {str(e)[:50]}...")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты: {len(available_models)}/{len(models_to_check)} моделей доступны")
    
    if available_models:
        print("\n✅ Доступные модели:")
        for model in available_models:
            print(f"  - {model}")
        
        print(f"\n💡 Рекомендуемая модель: {available_models[0]}")
    else:
        print("\n💥 Нет доступных моделей!")
        print("Проверьте:")
        print("  - Правильность API ключа")
        print("  - Баланс на OpenRouter")
        print("  - Доступность сервиса")


if __name__ == "__main__":
    asyncio.run(check_models())
