# user-api
A lightweight service for user management, authentication (JWT), and role-based access control. Built with Python, FastAPI, and Kafka integration.
### Первичный запуск базы данных
1. Склонировать репозиторий, зайти в папку с docker-compose.yml

	`git clone https://github.com/alenapoliakova/user-api.git`

2. Запустить контейнер с PostgreSQL

	`docker-compose up -d`
3. Проверить, что БД работает

	`docker ps`

4. Инициализировать базу данных (только при первом запуске)

	`docker exec -i postgresql-db-1 psql -U postgres -f dump.sql`
    
В дальнейшем можно включать/выключать контейнер `docker-compose up -d`/`docker-compose down`. Данные будут храниться в папке `pgdata`, которая создается при запуске контейнера.