# Быстрое исправление ошибки сборки на Railway

## Проблема
```
[строитель 2/5] COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/
Context canceled: Контекст отменен
```

## Решение

### Вариант 1: Использовать Dockerfile.simple (рекомендуется)
1. В настройках Railway укажите путь к Dockerfile:
   ```
   Dockerfile: Dockerfile.simple
   ```

### Вариант 2: Переименовать файлы
```bash
mv Dockerfile Dockerfile.uv
mv Dockerfile.simple Dockerfile
```

### Вариант 3: Использовать requirements.txt
1. Убедитесь, что `requirements.txt` существует
2. Railway автоматически использует его вместо pyproject.toml

## Проверка
После изменения перезапустите деплой в Railway.

## Альтернативные платформы
Если проблема сохраняется, рассмотрите:
- **Render** - более стабильная сборка
- **Fly.io** - отличная производительность
- **Google Cloud Run** - надежная инфраструктура
