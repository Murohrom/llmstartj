FROM python:3.11-slim

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копирование файлов конфигурации проекта
COPY pyproject.toml .python-version ./

# Установка зависимостей через uv
RUN uv sync --frozen --no-cache

# Копирование исходного кода
COPY src/ ./src/
COPY data/ ./data/

# Настройка переменных окружения
ENV PYTHONPATH=/app

# Запуск приложения через uv
CMD ["uv", "run", "src/bot.py"]
