# Руководство по настройке Railway

## Проблема: Отсутствуют переменные окружения

Если вы видите ошибку:
```
Ошибка конфигурации: Отсутствуют обязательные переменные окружения: TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY
```

Это означает, что в Railway не настроены переменные окружения.

## Пошаговая настройка Railway

### 1. Получение токенов

#### Telegram Bot Token
1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot` или используйте существующий бот
3. Скопируйте токен (формат: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### OpenRouter API Key
1. Зайдите на https://openrouter.ai/
2. Создайте аккаунт или войдите
3. Перейдите в раздел "API Keys"
4. Создайте новый ключ
5. Скопируйте API ключ

### 2. Настройка переменных в Railway

1. Откройте ваш проект в Railway
2. Перейдите в раздел "Variables"
3. Добавьте следующие переменные:

#### Обязательные переменные:
```
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
OPENROUTER_API_KEY=ваш_ключ_openrouter_здесь
```

#### Опциональные переменные:
```
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
CACHE_TTL_HOURS=24
LOG_LEVEL=INFO
DEBUG=false
```

### 3. Проверка настроек

После добавления переменных:
1. Нажмите "Save" для каждой переменной
2. Перезапустите деплой в Railway
3. Проверьте логи на наличие ошибок

## Примеры переменных

### Минимальная конфигурация:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Полная конфигурация:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
CACHE_TTL_HOURS=24
CACHE_DIR=data/cache
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
DEBUG=false
MAX_MESSAGE_LENGTH=4096
MAX_RETRIES=3
RETRY_DELAY=1
```

## Troubleshooting

### Проблема: Токен не работает
- Проверьте правильность токена
- Убедитесь, что бот не заблокирован
- Проверьте, что токен скопирован полностью

### Проблема: API ключ не работает
- Проверьте правильность API ключа
- Убедитесь, что у вас есть кредиты на OpenRouter
- Проверьте, что ключ активен

### Проблема: Переменные не сохраняются
- Убедитесь, что вы нажали "Save"
- Проверьте, что нет лишних пробелов
- Перезапустите деплой после сохранения

## Проверка работы

После настройки переменных бот должен:
1. Успешно запуститься без ошибок конфигурации
2. Подключиться к Telegram API
3. Отвечать на команды в Telegram

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте токены в репозиторий
- Используйте переменные окружения для всех секретов
- Регулярно обновляйте токены
- Ограничивайте доступ к API ключам
