#!/usr/bin/env python3
"""Скрипт для проверки Dockerfile"""

from pathlib import Path


def check_dockerfiles():
    """Проверяет все Dockerfile на наличие проблемных строк"""
    print("🔍 Проверка Dockerfile...")
    
    dockerfiles = [
        "Dockerfile",
        "Dockerfile.railway", 
        "Dockerfile.railway.simple",
        "Dockerfile.original"
    ]
    
    problematic_patterns = [
        "COPY data/ ./data/",
        "COPY данные/",
        "ls -la data/"
    ]
    
    all_good = True
    
    for dockerfile in dockerfiles:
        if not Path(dockerfile).exists():
            print(f"⚠️  {dockerfile} не найден")
            continue
            
        print(f"\n📄 Проверяю {dockerfile}:")
        
        with open(dockerfile, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_problems = False
        for pattern in problematic_patterns:
            if pattern in content:
                print(f"  ❌ Найдена проблемная строка: {pattern}")
                has_problems = True
                all_good = False
        
        if not has_problems:
            print(f"  ✅ {dockerfile} в порядке")
    
    print("\n" + "="*50)
    
    if all_good:
        print("🎉 Все Dockerfile исправлены!")
        return True
    else:
        print("💥 Есть проблемы в Dockerfile")
        return False


if __name__ == "__main__":
    check_dockerfiles()
