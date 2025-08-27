# Минимальный Dockerfile для Railway
FROM python:3.11-slim

WORKDIR /app

# Копирование файлов конфигурации
COPY requirements.txt ./

# Обновление pip и установка зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/

# Создание структуры данных
RUN mkdir -p data/cache

# Копирование данных
COPY data/ ./data/

# Настройка переменных окружения
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Запуск приложения
CMD ["python", "-m", "src.bot"]
