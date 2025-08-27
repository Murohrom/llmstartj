# Исправление ошибки с моделями OpenRouter

## 🚨 Проблема
```
Ошибка генерации ответа: Код ошибки: 404 - Не найдены конечные точки для meta-llama/llama-3.1-8b-instruct:free
```

## ✅ Решение

### 1. Изменена модель по умолчанию
- **Было**: `meta-llama/llama-3.1-8b-instruct:free`
- **Стало**: `openai/gpt-3.5-turbo`

### 2. Добавлен fallback механизм
Теперь бот автоматически переключается на доступные модели:
1. `openai/gpt-3.5-turbo` (основная)
2. `anthropic/claude-3-haiku` (fallback)
3. `google/gemini-pro` (fallback)
4. `meta-llama/llama-3.1-8b-instruct:free` (fallback)

### 3. Обновленные файлы
- `src/utils/config.py` - новая модель по умолчанию
- `src/services/llm_service.py` - fallback логика
- `env.example` - обновленный пример

## 🔧 Настройка

### Для локальной разработки
```bash
# В .env файле
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

### Для Railway
В переменных окружения Railway добавьте:
```
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

## 🧪 Проверка

### Запустите проверку моделей:
```bash
python check_models.py
```

### Результат должен показать доступные модели:
```
✅ Доступные модели:
  - openai/gpt-3.5-turbo
  - anthropic/claude-3-haiku
```

## 🎯 Результат
Теперь бот будет работать стабильно, автоматически переключаясь на доступные модели при ошибках!
