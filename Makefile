.PHONY: install test lint format type-check clean

# Установка зависимостей
install:
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

# Запуск тестов
test:
	pytest

# Линтинг
lint:
	isort --check-only app
	pylint app
	ruff check app

# Форматирование кода
format:
	isort app
	ruff format app

# Проверка типов
type-check:
	mypy app

# Очистка
clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Запуск всех проверок
check: lint format type-check test
