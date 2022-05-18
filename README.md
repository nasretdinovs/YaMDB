![workflow](https://github.com/nasretdinovs/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# YAMDB

Обзоры и мнения о медиа.

## Наполнение env-файла

 - DB_ENGINE - указываем систему управления базами данных
 - DB_NAME - имя базы данных
 - POSTGRES_USER - логин для подключения к базе данных
 - POSTGRES_PASSWORD - пароль для подключения к БД
 - DB_HOST - название сервиса (контейнера)
 - DB_PORT - порт для подключения к БД

Пример:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=Qwerty12345
DB_HOST=db
DB_PORT=5432
```

# Установка
Выполнить миграции, создать суперпользователя и собрать статику.
Для этого выполните по очереди команды в новом терминале:
```
sudo docker compose exec web python manage.py migrate
sudo docker compose exec web python manage.py createsuperuser
sudo docker compose exec web python manage.py collectstatic --no-input
```

## Запуск и остановка
Запуск производится командой:
```
sudo docker compose start
```
Остановка производится командой:
```
sudo docker compose stop
```
После запуска локального сервера документация API доступна по адресу [http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)

# Работа с базой данных
Команда для копирования файла на сервер по SSH:
```
scp fixtures.json USERNAME@PUBLIC-IP:/home/USERNAME/
```

Команда для копирования файла с данными в контейнер:
```
sudo docker cp fixtures.json USERNAME-web-1:app
```

Для заполнения базы данными надо выполнить по очереди команды:
```
sudo docker compose exec web python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
sudo docker compose exec web python manage.py loaddata fixtures.json
```

Команда для создания резервной копии базы:
```
sudo docker compose exec web python manage.py loaddata fixtures.json
```


## Технологии

Приложение работает на
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).


## Разработчики

Проект разработан
- [Александр Рубцов](https://github.com/FinemechanicPub)
- [Анастасия Дементьева](https://github.com/Nastasia153)
- [Виталий Насретдинов](https://github.com/nasretdinovs)


## License
[MIT](https://choosealicense.com/licenses/mit/)
