# Users API

REST API для управления пользователями с использованием FastAPI и PostgreSQL.

## Разработка

### Установка зависимостей

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте его:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
# Только для продакшена
pip install -r requirements.txt

# Для разработки (включая тесты и линтеры)
pip install -r requirements.txt -r requirements.dev.txt
```

### Проверка кода

В проекте настроены следующие инструменты для проверки качества кода:

#### Запуск всех проверок

```bash
make check
```

Эта команда последовательно запустит все проверки:
- Линтеры (ruff, pylint)
- Проверка типов (mypy)
- Тесты (pytest)

#### Запуск отдельных проверок

```bash
# Запуск тестов
make test

# Запуск линтеров
make lint

# Проверка типов
make type-check

# Форматирование кода
make format
```

#### Очистка кеша и временных файлов

```bash
make clean
```

### Рекомендации по разработке

1. Перед коммитом всегда запускайте `make check` для проверки кода
2. Используйте `make format` для автоматического форматирования кода
3. Добавляйте тесты для нового функционала
4. Следите за покрытием кода тестами

## Запуск приложения

```bash
uvicorn app.main:app --reload
```

API будет доступно по адресу: http://localhost:8000

Документация API (Swagger): http://localhost:8000/docs

## Требования

- Docker
- Docker Compose
- Python 3.12 (для локальной разработки)

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/alenapoliakova/user-api.git
cd user-api
```

2. Запустите контейнеры:
```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8000

### Структура проекта

```
user-api/
├── app/
│   ├── api/              # API эндпоинты
│   ├── core/             # Основные настройки
│   ├── db/               # Работа с базой данных
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   └── main.py           # Точка входа
├── tests/                # Тесты
├── docker-compose.yml    # Конфигурация Docker
├── Dockerfile           # Конфигурация контейнера
└── requirements.txt     # Зависимости
```

### База данных

- PostgreSQL 16
- Автоматическое создание таблиц при запуске

### API Документация

После запуска сервиса доступны:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## CI/CD

Проект использует GitHub Actions для:
- Запуска тестов
- Проверки типов
- Линтинга
- Форматирования кода

## Лицензия

MIT
