# FinAPI
Асинхронное REST API для управления электронными кошельками с защитой от конкуретных операций. Выполнено в рамках тестового задания.

## Стек

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-100000?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Kelvich322/FinAPI.git
cd FinAPI
```

### 2. Запуск через Docker
```bash
# Запуск всего приложения, вместе с БД. Логи будут выведены в консоль.
docker compose up --build
```

### 3. Локальная разработка
```bash
# Установка зависимостей
poetry install

# Активация вирт.окружения:
poetry env activate # Результат выполнения нужно скопировать и вставить в консоль

# Запуск базы данных
docker compose up -d db

# Применение миграций
alembic upgrade head

# Запуск приложения
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Документация:
После запуска приложения документация доступна по адресам:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

## Эндпоинты

### Создание кошелька:
```http
POST /api/v1/wallets
```
### Получение информации о кошельке:
```http
GET /api/v1/wallets/{wallet_id}
```
### Выполнение операции:
```http
POST /api/v1/wallets/{wallet_id}/operation
```
#### Body:
```json
{
  "operation_type": "DEPOSIT|WITHDRAW",
  "amount": "1000.00"
}
```

## Тестирование

### Запуск тестов

```bash
pytest -v
```

## Автор
* Кельвич Богдан - https://github.com/Kelvich322
