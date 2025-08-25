# Anime Bot - LLM-ассистент для подбора аниме

## Описание
Telegram бот для подбора аниме с использованием LLM (OpenRouter API). Бот общается в стиле персонажа Сайтамы из аниме "Ванпанчмен".

## Статус проекта
✅ **MVP завершен** - бот готов к продакшену

## Возможности
- 🤖 Персональные рекомендации аниме через LLM
- 💬 Диалог в стиле Сайтамы
- 📚 Специализированные команды (/top, /new, /classic)
- 🔄 Пагинация длинных списков
- 💾 Кэширование ответов
- 🧠 Память о контексте диалога
- 📱 Inline-кнопки для удобной навигации

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

# Или через Docker Compose
docker-compose up --build

# Или через Docker
docker build -t anime-bot .
docker run --env-file .env anime-bot
```

## Деплой

### Поддерживаемые платформы
- 🚂 **Railway** - рекомендуемая платформа
- 🎨 **Render** - альтернативная платформа
- ⚡ **Heroku** - классическая платформа
- 🖥️ **VPS** - полный контроль

### Быстрый деплой на Railway
1. Fork этого репозитория
2. Создайте аккаунт на [Railway](https://railway.app/)
3. Подключите ваш fork
4. Добавьте переменные окружения:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENROUTER_API_KEY`
5. Деплой произойдет автоматически

Подробные инструкции: [docs/deployment.md](docs/deployment.md)

## Документация

- 📖 [Руководство по деплою](docs/deployment.md)
- 🔧 [Устранение неполадок](docs/troubleshooting.md)
- 🤖 [Создание бота](doc/guides/telegram_bot_creation.md)

### Облачные платформы для деплоя

- 🚂 [Railway - рекомендуемая платформа](docs/railway_deployment_guide.md)
- 🎨 [Render - альтернативная платформа](docs/render_deployment_guide.md)
- 🚀 [Fly.io - для продвинутых](docs/fly_deployment_guide.md)
- 📊 [Исследование платформ](docs/cloud_platforms_research.md)
- 🎯 [Выбор платформы](docs/cloud_deployment_choice.md)

## Архитектура

```
src/
├── bot.py                 # Точка входа
├── handlers/              # Обработчики команд
│   ├── start.py          # Команды /start, /help, /top, /new, /classic
│   └── anime.py          # Обработка текстовых сообщений
├── services/             # Бизнес-логика
│   ├── llm_service.py    # Интеграция с OpenRouter API
│   ├── cache_service.py  # Кэширование ответов
│   ├── user_state_service.py # Управление состоянием пользователей
│   └── pagination_service.py # Пагинация списков
└── utils/                # Утилиты
    ├── config.py         # Конфигурация
    ├── logger.py         # Логирование
    ├── prompts.py        # Промпты для LLM
    ├── message_utils.py  # Утилиты для сообщений
    └── health_check.py   # Мониторинг здоровья
```

## Технологии

- **Python 3.11+** - основной язык
- **aiogram 3.x** - Telegram Bot API
- **OpenRouter API** - LLM интеграция
- **uv** - управление зависимостями
- **Docker** - контейнеризация
- **GitHub Actions** - CI/CD

## Лицензия

MIT License

---
*Разработано в рамках интенсива LLM Start*
