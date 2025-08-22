# Домашнее задание LLM Start

## Студент
**Фамилия Имя:** [Укажите свои фамилию и имя]

## Статус выполнения
🟡 В процессе

## Описание
Репозиторий содержит выполнение домашнего задания после прохождения интенсива LLM Start.

## Проект
Разработка LLM-ассистента для подбора аниме в Telegram.

## Быстрый старт

### Установка зависимостей
```bash
# Установка uv (если еще не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Клонирование и настройка проекта
git clone <repository-url>
cd llmstartj

# Синхронизация зависимостей
uv sync
```

### Настройка переменных окружения
```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл со своими токенами
# TELEGRAM_BOT_TOKEN=ваш_токен_бота
# OPENROUTER_API_KEY=ваш_ключ_openrouter
```

### Запуск проекта
```bash
# Локальный запуск
uv run src/bot.py

# Или через Docker
docker build -t anime-bot .
docker run --env-file .env anime-bot
```

---
*Интенсив LLM Start*
