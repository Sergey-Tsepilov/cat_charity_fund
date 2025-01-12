# QRKot

## Технологии:

- Python 3.9.13
- FastAPI 0.78.0

## Установка (Windows):

1. Клонирование репозитория

```
git clone https://github.com/Sergey-Tsepilov/cat_charity_fund.git
```

2. Переход в директорию cat_charity_fund

```
cd cat_charity_fund
```

3. Создание виртуального окружения

```
python -m venv venv
```

4. Активация виртуального окружения

```
source venv/Scripts/activate
```

5. Обновите pip

```
python -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt
```

7. Создание и настройка базы данных

```
APP_TITLE=...
APP_DESCRIPTION=...
DATABASE_URL=...
SECRET=...
FIRST_SUPERUSER_EMAIL=...
FIRST_SUPERUSER_PASSWORD=...
```

8. Запуск сервера с автоматическим рестартом

```
uvicorn app.main:app --reload
```
