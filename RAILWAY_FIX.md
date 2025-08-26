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

## Проблема 3: Ошибка копирования папки data
```
[6/6] КОПИРОВАТЬ данные/ ./data/
Не удалось вычислить контрольную сумму ref lw7qxevaknn21qsgydh74uxhb::8clu7x9mvk72lw319AGUXQbek: "/data": не найдено
```

## Решения

### Вариант 1: Использовать Dockerfile.simple (рекомендуется)
1. Переименуйте файлы:
   ```bash
   mv Dockerfile Dockerfile.original
   mv Dockerfile.simple Dockerfile
   ```

### Вариант 2: Настроить в Railway
В настройках проекта Railway укажите:
```
Dockerfile: Dockerfile.simple
```

### Вариант 3: Использовать .dockerignore
Убедитесь, что файл `.dockerignore` существует и исключает ненужные файлы.

## Почему это работает
- Убрали проблемную команду COPY data/
- Создаем папку data/cache через RUN mkdir
- Исключаем ненужные файлы через .dockerignore
- Минимальный размер образа
- Меньше потребление памяти при сборке

## Проверка
После изменения перезапустите деплой в Railway.

## Альтернативные платформы
Если проблема сохраняется:
- **Render** - более стабильная сборка
- **Fly.io** - отличная производительность
- **Google Cloud Run** - надежная инфраструктура
