# Многоэтапная сборка для оптимизации размера образа
FROM python:3.11-slim as builder

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копирование файлов конфигурации проекта
COPY pyproject.toml uv.lock ./

# Установка зависимостей через uv
RUN uv sync --frozen --no-cache

# Финальный образ
FROM python:3.11-slim as runtime

WORKDIR /app

# Копирование виртуального окружения из builder
COPY --from=builder /app/.venv /app/.venv

# Копирование исходного кода
COPY src/ ./src/
COPY data/ ./data/

# Настройка переменных окружения
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Создание пользователя без root прав
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Переключение на пользователя app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Запуск приложения
CMD ["python", "src/bot.py"]
