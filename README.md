### Используемые технологии:

- Python 3.13
- Django 4.2
- jQuery 3.6
- PostgreSQL 15
- Gunicorn 23.0
- Docker

### Запуск:
Клонировать репозиторий:
```
git clone https://github.com/Randy-Colt/files_converter.git
cd files_converter/
```
Запустить приложение:
```
docker-compose up
```

Приложение будет доступно по адресу:
```
http://127.0.0.1:8000/albums/
```

### Запуск без докера
В файле example.env установите переменную 
```
SQLITE=True
```
Установите зависимости приложения в виртуальное окружение:
```
pip install -r requirements.txt
```
В директории converter_webapp выполните миграции и запустите приложение:
```
python manage.py migrate
python manage.py runserver
```
