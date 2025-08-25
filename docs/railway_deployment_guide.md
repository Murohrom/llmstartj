# Руководство по развертыванию на Railway

## Проблемы и решения

### Ошибка сборки с uv
Если возникает ошибка:
```
[строитель 2/5] COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/
Context canceled: Контекст отменен
```

**Решение:** Используйте `Dockerfile.simple` вместо основного `Dockerfile`.

## Пошаговое развертывание

### 1. Подготовка репозитория

Убедитесь, что в корне проекта есть файлы:
- `Dockerfile.simple` (для Railway)
- `pyproject.toml`
- `src/bot.py`
- `env.example`

### 2. Создание проекта на Railway

1. Зайдите на [railway.app](https://railway.app)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Подключите ваш GitHub репозиторий

### 3. Настройка переменных окружения

В настройках проекта добавьте переменные:
```
TELEGRAM_BOT_TOKEN=your_bot_token
OPENROUTER_API_KEY=your_api_key
```

### 4. Настройка Dockerfile

Если основной Dockerfile не работает, Railway автоматически попробует `Dockerfile.simple`.

### 5. Деплой

1. Railway автоматически обнаружит Dockerfile
2. Нажмите "Deploy" в интерфейсе
3. Дождитесь завершения сборки

## Альтернативные решения

### Вариант 1: Использовать Dockerfile.simple
Переименуйте `Dockerfile.simple` в `Dockerfile`:
```bash
mv Dockerfile.simple Dockerfile
```

### Вариант 2: Настроить в Railway
В настройках проекта Railway укажите путь к Dockerfile:
```
Dockerfile: Dockerfile.simple
```

### Вариант 3: Использовать requirements.txt
Создайте `requirements.txt`:
```txt
aiogram>=3.0.0
openai
python-dotenv
aiofiles
```

И используйте простой Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY data/ ./data/
CMD ["python", "src/bot.py"]
```

## Мониторинг

После деплоя проверьте:
1. Логи сборки в Railway
2. Статус контейнера
3. Логи приложения
4. Работу health check

## Troubleshooting

### Ошибка "Context canceled"
- Используйте `Dockerfile.simple`
- Убедитесь в стабильности интернет-соединения
- Попробуйте перезапустить деплой

### Ошибка зависимостей
- Проверьте `pyproject.toml`
- Убедитесь в совместимости версий Python

### Ошибка переменных окружения
- Проверьте все обязательные переменные
- Убедитесь в правильности токенов
