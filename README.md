[![test_bewise workflow](https://github.com/themasterid/test_bewise/actions/workflows/test_bewise.yml/badge.svg)](https://github.com/themasterid/test_bewise/actions/workflows/test_bewise.yml)
# Тестовое задание bewise

Задание доступно по адресу http://хх.хх.хх.хх/api/post/ до 14.07.2022 г. 
Статус на 15.08.2022 (отключен).

# Стек
- Python 3.10
- Docker
- docker-compose
- Django 3.2.15
- Django REST framework
- CI/CD
- PostgreSQL
- Yandex.Cloud

## Описание задания bewise:
- В сервисе реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer}.
- После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
- Далее, полученные ответы сохраняются в базе данных из п. 1, причем сохраняется как минимум следующая информация: ID вопроса, Текст вопроса, Текст ответа, Дата создания вопроса.
- Если в БД имеется такой же вопрос, к публичному API с викторинами выполняются дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
- Ответом на запрос из п.2.a предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.


## Запуск API в облаке с использованием CI/CD:

Установить docker, docker-compose на сервере виртуальной машины Yandex.Cloud:

```bash
ssh username@ip
```

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```

```bash
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh 
```

```bash
get-docker.sh && sudo rm get-docker.sh
```

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

Создаем папку infra на виртуальной машине:

```bash
mkdir infra
```

- Переносим файлы docker-compose.yml, default.conf и .env на сервер в папку infra.

```bash
scp .env username@server_ip:/home/username/infra/
```

```bash
scp docker-compose.yml username@server_ip:/home/username/infra/
```

```bash
scp default.conf username@server_ip:/home/username/infra/
```

- Так же, можно создать пустой файл .env в директории infra, позже в него будем добавлять данные с git secrets:

```bash
touch .env
```
- Заполнить в настройках репозитория секреты в .env из Secrets GitHub:

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='bewise'
POSTGRES_USER='bewise_u'
POSTGRES_PASSWORD='put_your_password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```

- Запускаем контейнеры находясь в папке infra:
```bash
sudo docker-compose up -d --build
```

- Затем применяем миграции, собираем статику:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```
```bash
sudo docker-compose exec backend python manage.py migrate --noinput 
```
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

API будет доступно по адресу: http://your_ip/api/post/

- Остановить:
```bash
sudo docker-compose stop/down
```

## Запуск проекта в dev-режиме

- Клонируем репозиторий:

```bash
git clone git@github.com:themasterid/test_bewise.git
```

Переходим в папку с проектом:

```bash
cd test_bewise
```

- Установить и активировать виртуальное окружение (git bash):

```bash
python3 -m venv venv
```

Windows:
```bash
source venv/Scripts/activate
```

Linux:
```bash
source venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
cd bewise
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Создайте базу и пользователя в PosgreSQL:

Linux:
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE bewise_test;
```
```sql
CREATE USER tuser_bewise WITH ENCRYPTED PASSWORD '@test#bewise';
```
```sql
GRANT ALL PRIVILEGES ON DATABASE bewise_test TO tuser_bewise;
```

Windows, запустите SQL Shell (psql):
```sql
CREATE DATABASE bewise_test;
```
```sql
CREATE USER tuser_bewise WITH ENCRYPTED PASSWORD '@test#bewise';
```
```sql
GRANT ALL PRIVILEGES ON DATABASE bewise_test TO tuser_bewise;
```

- Прописываем данные для работы в dev режиме в .env файл (там где у нас файл settings.py):

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='bewise_test'
POSTGRES_USER='tuser_bewise'
POSTGRES_PASSWORD='@test#bewise'
DB_HOST='127.0.0.1'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=True
```

- Выполняем миграции, собираем статику, создаем администратора:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
```

- Запускаем сервер:
```bash
python manage.py runserver
```

### Документация к API доступна после запуска
```text
http://127.0.0.1:8000/api/post/
```

Автор: [Клепиков Дмитрий](https://github.com/themasterid)
