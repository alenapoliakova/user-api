# Users API

API сервис для управления пользователями, построенный на FastAPI.

## Требования

- Docker
- Docker Compose
- Python 3.12 (для локальной разработки)

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/alenapoliakova/user-api.git
cd users-api
```

2. Запустите контейнеры:
```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8000

### Структура проекта

```
users-api/
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
