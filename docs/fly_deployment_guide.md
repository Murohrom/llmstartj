# Пошаговая инструкция по деплою на Fly.io

## Обзор

Fly.io - это современная платформа с глобальным распределением и отличной производительностью. Подходит для более продвинутых пользователей, которые хотят максимальную производительность.

## Предварительные требования

### 1. Подготовка проекта
- ✅ Проект в GitHub репозитории
- ✅ Dockerfile в корне проекта
- ✅ fly.toml конфигурация (создадим)

### 2. Необходимые токены
- **Telegram Bot Token** - от @BotFather
- **OpenRouter API Key** - от https://openrouter.ai/
- **Fly.io API Token** - получим в процессе настройки

## Пошаговый процесс деплоя

### Шаг 1: Установка Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### Шаг 2: Создание аккаунта

1. Перейдите на [Fly.io](https://fly.io/)
2. Нажмите "Get Started"
3. Создайте аккаунт
4. Подтвердите email

### Шаг 3: Авторизация в CLI

```bash
fly auth login
```

Следуйте инструкциям в браузере для авторизации.

### Шаг 4: Создание приложения

```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/anime-bot.git
cd anime-bot

# Создайте приложение
fly launch
```

### Шаг 5: Настройка fly.toml

Создайте файл `fly.toml` в корне проекта:

```toml
app = "your-anime-bot-name"
primary_region = "iad"  # Вашингтон, DC

[build]

[env]
  TELEGRAM_BOT_TOKEN = ""
  OPENROUTER_API_KEY = ""
  OPENROUTER_MODEL = "openai/gpt-3.5-turbo"
  MAX_RETRIES = "3"
  RETRY_DELAY = "1"
  CACHE_TTL = "3600"
  LOG_LEVEL = "INFO"

[http_service]
  internal_port = 10000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"

[machine]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### Шаг 6: Настройка переменных окружения

```bash
# Установите переменные окружения
fly secrets set TELEGRAM_BOT_TOKEN="ваш_токен_бота"
fly secrets set OPENROUTER_API_KEY="ваш_ключ_openrouter"
fly secrets set OPENROUTER_MODEL="openai/gpt-3.5-turbo"
fly secrets set MAX_RETRIES="3"
fly secrets set RETRY_DELAY="1"
fly secrets set CACHE_TTL="3600"
fly secrets set LOG_LEVEL="INFO"
```

### Шаг 7: Деплой

```bash
# Разверните приложение
fly deploy
```

### Шаг 8: Проверка статуса

```bash
# Проверьте статус приложения
fly status

# Посмотрите логи
fly logs

# Откройте приложение в браузере
fly open
```

## Особенности Fly.io

### Глобальное распределение

- Приложение развертывается в ближайшем к вам регионе
- Автоматическое масштабирование
- Низкая задержка для пользователей

### Лимиты бесплатного тарифа

- **3 виртуальные машины** - достаточно для бота
- **3GB хранилища** - для кэша и логов
- **160GB исходящего трафика** - много для бота
- **Автоматическое масштабирование** - 0-3 машины

## Мониторинг

### Просмотр логов

```bash
# Логи в реальном времени
fly logs

# Логи с фильтрацией
fly logs --app your-anime-bot-name

# Логи за последние 10 минут
fly logs --since 10m
```

### Статус приложения

```bash
# Общий статус
fly status

# Детальная информация
fly status --all
```

### Масштабирование

```bash
# Увеличить количество машин
fly scale count 2

# Увеличить ресурсы
fly scale memory 1024

# Автоматическое масштабирование
fly scale count 0-3
```

## Troubleshooting

### Проблема: Приложение не запускается

**Решение:**
```bash
# Проверьте логи
fly logs

# Проверьте статус
fly status

# Перезапустите приложение
fly restart
```

### Проблема: Ошибки сборки

**Решение:**
```bash
# Очистите кэш сборки
fly deploy --no-cache

# Проверьте Dockerfile
docker build -t test .
```

### Проблема: Высокая стоимость

**Решение:**
```bash
# Уменьшите количество машин
fly scale count 1

# Уменьшите ресурсы
fly scale memory 256

# Включите автостоп
fly scale count 0-1
```

## Оптимизация для Fly.io

### 1. Настройка Dockerfile

```dockerfile
# Оптимизируйте размер образа
FROM python:3.11-slim as builder
# ... многоэтапная сборка

# Установите правильный порт
EXPOSE 10000

# Добавьте health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"
```

### 2. Настройка портов

```python
import os
port = int(os.getenv('PORT', 10000))
```

### 3. Оптимизация ресурсов

```toml
[machine]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512  # Минимум для Python
```

## Стоимость

- **Бесплатно** - 3 VM, 3GB хранилища, 160GB трафика
- **Платно** - $1.94/месяц за дополнительную VM

## Преимущества Fly.io

- ✅ Глобальное распределение
- ✅ Отличная производительность
- ✅ Щедрый бесплатный тариф
- ✅ CLI инструменты
- ✅ Автоматическое масштабирование

## Недостатки

- ❌ Сложнее в настройке
- ❌ Требует CLI
- ❌ Меньше GUI инструментов

## Заключение

Fly.io - отличный выбор для тех, кто хочет максимальную производительность и глобальное распределение. Требует больше технических знаний, но предоставляет мощные возможности.

## Полезные ссылки

- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io CLI Reference](https://fly.io/docs/flyctl/)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
