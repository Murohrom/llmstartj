# Makefile для Сайтама Бота - LLM-ассистента для подбора аниме
# Использует uv для управления зависимостями и виртуальным окружением

.PHONY: help install dev run stop test clean lint format check

# Переменные
PYTHON_FILES = src/ tests/
PID_FILE = .bot.pid

# Показать справку по командам
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "  install    - Установить зависимости проекта"
	@echo "  dev        - Установить зависимости для разработки"
	@echo "  run        - Запустить бота"
	@echo "  stop       - Остановить бота"
	@echo "  test       - Запустить тесты"
	@echo "  lint       - Проверить код с помощью flake8 и mypy"
	@echo "  format     - Отформатировать код с помощью black и isort"
	@echo "  check      - Проверить код (lint + test)"
	@echo "  clean      - Очистить временные файлы"
	@echo ""

# Установить основные зависимости
install:
	@echo "📦 Установка зависимостей..."
	uv sync --no-dev

# Установить зависимости для разработки
dev:
	@echo "🛠️ Установка зависимостей для разработки..."
	uv sync

# Запустить бота
run:
	@echo "🤖 Запуск Сайтама Бота..."
	@if [ -f $(PID_FILE) ]; then \
		echo "⚠️  Бот уже запущен (PID: $$(cat $(PID_FILE)))"; \
		echo "Используйте 'make stop' для остановки"; \
		exit 1; \
	fi
	@echo "Убедитесь, что .env файл настроен с токеном Telegram бота!"
	uv run python src/bot.py & echo $$! > $(PID_FILE)
	@echo "✅ Бот запущен (PID: $$(cat $(PID_FILE)))"
	@echo "📝 Для остановки используйте: make stop"

# Остановить бота
stop:
	@if [ ! -f $(PID_FILE) ]; then \
		echo "❌ Бот не запущен"; \
		exit 1; \
	fi
	@echo "⏹️  Остановка бота..."
	@PID=$$(cat $(PID_FILE)); \
	if kill -0 $$PID 2>/dev/null; then \
		kill $$PID; \
		echo "✅ Бот остановлен (PID: $$PID)"; \
	else \
		echo "⚠️  Процесс с PID $$PID не найден"; \
	fi
	@rm -f $(PID_FILE)

# Запустить тесты
test:
	@echo "🧪 Запуск тестов..."
	uv run python -m pytest tests/ -v --tb=short

# Проверка кода с помощью линтеров
lint:
	@echo "🔍 Проверка кода..."
	@echo "Запуск flake8..."
	uv run flake8 $(PYTHON_FILES)
	@echo "Запуск mypy..."
	uv run mypy $(PYTHON_FILES)

# Форматирование кода
format:
	@echo "✨ Форматирование кода..."
	@echo "Запуск isort..."
	uv run isort $(PYTHON_FILES)
	@echo "Запуск black..."
	uv run black $(PYTHON_FILES)

# Полная проверка (линтинг + тесты)
check: lint test
	@echo "✅ Все проверки пройдены!"

# Очистка временных файлов
clean:
	@echo "🧹 Очистка временных файлов..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f $(PID_FILE)
	rm -rf .coverage htmlcov/
	@echo "✅ Очистка завершена"

# Показать статус бота
status:
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		if kill -0 $$PID 2>/dev/null; then \
			echo "✅ Бот работает (PID: $$PID)"; \
		else \
			echo "❌ PID файл существует, но процесс не найден"; \
			rm -f $(PID_FILE); \
		fi \
	else \
		echo "❌ Бот не запущен"; \
	fi

# Перезапустить бота
restart: stop run
	@echo "🔄 Бот перезапущен"
