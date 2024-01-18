***
_Репозиторий на Github [ссылка](https://github.com/JuliaBars/platform_for_recipes)._

## Recipes and more

[![workflow](https://github.com/JuliaBars/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/JuliaBars/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

Сайт продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на авторов любимых рецептов.

----
## Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

---
#### Развернуть проект локально:
- склонируйте проект
```
git clone https://github.com/JuliaBars/platform_for_recipes
```
- Добавьте файл .env в папку infra/
```DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=foodgram
DB_HOST=db
DB_PORT=5432
DEBUG=False
```
- Запустите docker compose local из директории infra/
```
docker compose -f docker-compose-local.yml up -d
```
- Если хотите сразу заполнить БД рецептами, то выполните команду из папки infra/:
```
./load_db
```
- Если нужна БД без рецептов, то можно загрузить только ингредиенты, выполните команду из директории infra/:
```
./load_ingredients
```
**После первой загрузки все данные будут храниться в volume.**

Посмотреть докуметацию к АПИ при локальном запуске можно по адресу:
```
http://localhost/api/docs/
```

---
#### Развернуть проект на удаленном сервере:

- Клонировать репозиторий:

```
git clone git@github.com:JuliaBars/foodgram-project-react.git
```

- Установить на сервере Docker, Docker Compose.
- Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra:

```
scp docker-compose.yml nginx.conf username@IP:/home/username/ 
```

- Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:

```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID вашего телеграм-аккаунта
TELEGRAM_TOKEN          # токен вашего телеграм-бота

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```

- Создать и запустить контейнеры Docker

```
sudo docker-compose up -d
```

- После успешной сборки, в контейнере backend выполнить миграции, и собрать статику.

----
Для загрузки тестовой БД из контейнера backend выполните команду:

```
python manage.py loaddata fixtures.json
```

---
В проекте настроен CI/CD с гитхаб Actions.
После каждого обновления репозитория (push в ветку main) будет происходить:

1. Проверка кода на соответствие стандарту PEP8
2. Сборка и доставка докер-образа backend на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram об успешном выполнении workflow
