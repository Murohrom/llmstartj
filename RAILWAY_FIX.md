# Быстрое исправление ошибки сборки на Railway

## Проблема 1: Ошибка uv
```
[строитель 2/5] COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/
Context canceled: Контекст отменен
```

## Проблема 2: Нехватка памяти (exit code 137)
```
RUN apt-get update & apt-get install -y curl & rm -rf /var/lib/apt/lists/*
exit code: 137: context canceled
```

## Решения

### Вариант 1: Использовать Dockerfile.minimal (рекомендуется)
1. Переименуйте файлы:
   ```bash
   mv Dockerfile Dockerfile.original
   mv Dockerfile.minimal Dockerfile
   ```

### Вариант 2: Использовать Dockerfile.simple
1. Переименуйте файлы:
   ```bash
   mv Dockerfile Dockerfile.original
   mv Dockerfile.simple Dockerfile
   ```

### Вариант 3: Настроить в Railway
В настройках проекта Railway укажите:
```
Dockerfile: Dockerfile.minimal
```

## Почему это работает
- Убрали системные зависимости (apt-get)
- Убрали uv и используем только pip
- Минимальный размер образа
- Меньше потребление памяти при сборке

## Проверка
После изменения перезапустите деплой в Railway.

## Альтернативные платформы
Если проблема сохраняется:
- **Render** - более стабильная сборка
- **Fly.io** - отличная производительность
- **Google Cloud Run** - надежная инфраструктура
