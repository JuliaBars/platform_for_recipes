***
_Репозиторий на Github [ссылка](https://github.com/JuliaBars/foodgram-project-react)._

### Первый этап: ревью кода проекта

Чтобы получить документацию к проекту:

```
В папке infra выполните команду docker-compose up
```
Пройдите по [ссылке](http://localhost/api/docs/redoc.html).


Основные эндпоинты проекта:

```
http://localhost/api/users/
http://localhost/api/auth/token/login/
http://localhost/api/tags/
http://localhost/api/recipes/
http://localhost/api/recipes/download_shopping_cart/
http://localhost/api/recipes/{id}/favorite/
http://localhost/api/users/subscriptions/
http://localhost/api/ingredients/
```

В папке backend размещен дамп тестовой БД.
Из директории с файлом manage.py выполните команду:

```
python manage.py loaddata fixtures.json
```

### Шаблон заполнения .env в директории infra/.env

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Автор

Студент Я.Практикум - _Юлия Орлова_
