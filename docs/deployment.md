# Деплой Anime Bot

## Обзор

Этот документ описывает процесс деплоя Anime Bot на различные платформы.

## Подготовка к деплою

### 1. Переменные окружения

Создайте файл `.env` со следующими переменными:

```env
# Telegram Bot Token (получите у @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenRouter API Key (получите на https://openrouter.ai/)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Модель LLM (по умолчанию: openai/gpt-3.5-turbo)
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# Настройки retry
MAX_RETRIES=3
RETRY_DELAY=1

# Настройки кэша (в секундах)
CACHE_TTL=3600

# Уровень логирования
LOG_LEVEL=INFO
```

### 2. Локальная разработка с Docker

```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f anime-bot

# Остановка
docker-compose down
```

## Деплой на Railway

### 1. Подготовка

1. Создайте аккаунт на [Railway](https://railway.app/)
2. Подключите ваш GitHub репозиторий
3. Создайте новый проект

### 2. Настройка переменных окружения

В настройках проекта Railway добавьте переменные окружения:

- `TELEGRAM_BOT_TOKEN`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL` (опционально)
- `MAX_RETRIES` (опционально)
- `RETRY_DELAY` (опционально)
- `CACHE_TTL` (опционально)
- `LOG_LEVEL` (опционально)

### 3. Деплой

Railway автоматически обнаружит Dockerfile и выполнит деплой.

## Деплой на Render

### 1. Подготовка

1. Создайте аккаунт на [Render](https://render.com/)
2. Подключите ваш GitHub репозиторий
3. Создайте новый Web Service

### 2. Настройка

- **Build Command**: `docker build -t anime-bot .`
- **Start Command**: `docker run -p 10000:10000 anime-bot`
- **Environment**: Docker

### 3. Переменные окружения

Добавьте те же переменные окружения, что и для Railway.

## Деплой на Heroku

### 1. Подготовка

1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Создайте аккаунт на [Heroku](https://heroku.com/)

### 2. Настройка

```bash
# Логин в Heroku
heroku login

# Создание приложения
heroku create your-anime-bot-name

# Добавление переменных окружения
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set OPENROUTER_API_KEY=your_key

# Деплой
git push heroku main
```

## Деплой на VPS

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Деплой

```bash
# Клонирование репозитория
git clone https://github.com/your-username/anime-bot.git
cd anime-bot

# Создание .env файла
cp env.example .env
# Отредактируйте .env файл

# Запуск
docker-compose up -d
```

## Мониторинг и логи

### Просмотр логов

```bash
# Docker Compose
docker-compose logs -f anime-bot

# Docker
docker logs -f anime-bot

# Railway
railway logs

# Render
# Логи доступны в веб-интерфейсе
```

### Health Check

Бот включает встроенный health check, который проверяет работоспособность каждые 30 секунд.

## Troubleshooting

### Проблемы с переменными окружения

1. Убедитесь, что все переменные окружения установлены
2. Проверьте правильность токенов
3. Убедитесь, что бот не заблокирован

### Проблемы с API

1. Проверьте баланс на OpenRouter
2. Убедитесь, что API ключ действителен
3. Проверьте лимиты запросов

### Проблемы с Telegram

1. Убедитесь, что бот не заблокирован пользователями
2. Проверьте настройки приватности бота
3. Убедитесь, что токен бота действителен

## Обновление

### Автоматическое обновление

При использовании GitHub Actions обновления происходят автоматически при push в main ветку.

### Ручное обновление

```bash
# Docker Compose
docker-compose pull
docker-compose up -d

# Docker
docker pull your-image
docker stop anime-bot
docker rm anime-bot
docker run -d --name anime-bot your-image
```

## Безопасность

1. Никогда не коммитьте `.env` файл
2. Используйте секреты в CI/CD
3. Регулярно обновляйте зависимости
4. Мониторьте логи на подозрительную активность
