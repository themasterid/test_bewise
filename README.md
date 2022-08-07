[![test_bewise workflow](https://github.com/themasterid/test_bewise/actions/workflows/test_bewise.yml/badge.svg)](https://github.com/themasterid/test_bewise/actions/workflows/test_bewise.yml)
# Тестовое задание bewise

Задание доступно по адресу http://62.84.115.143 до 14.07.2022 г.

# Стек
- Python 3.10
- Docker
- docker-compose
- Django 3
- Django REST framework
- CI/CD
- PostgreSQL
- Yandex.Cloud

## Описание задания bewise
- В сервисе реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer}.
- После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
- Далее, полученные ответы сохраняются в базе данных из п. 1, причем сохраняется как минимум следующая информация: ID вопроса, Текст вопроса, Текст ответа, Дата создания вопроса.
- Если в БД имеется такой же вопрос, к публичному API с викторинами выполняются дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
- Ответом на запрос из п.2.a предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.


## Запуск с использованием CI/CD

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
- Заполнить в настройках репозитория секреты в .env

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='bewise_test'
POSTGRES_USER='tuser_bewise'
POSTGRES_PASSWORD='@test#bewise'
DB_HOST='127.0.0.1'
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
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

API будет доступно по адресу: http://your_ip/api/post/

- Остановить:
```bash
sudo docker-compose stop/down
```


## Запуск проекта через Docker на локальной машине:
- Устанавливаем Docker на localhost, пример для Linux:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- В папке infra переименовываем файл .env_esample в .env и заполняем своими данными согласно шаблона:

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='bewise_test'
POSTGRES_USER='tuser_bewise'
POSTGRES_PASSWORD='@test#bewise'
DB_HOST='127.0.0.1'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```

- Затем в папке infra выполнить команду, запускаем контейнеры:

```bash
sudo docker-compose up -d --build
```

Для доступа к контейнеру backend выполните следующие команды, это позволит собрать статику, сделать миграции и если нужно создать администратора, для доступа в админку:

```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

API доступно на локальной машине по адресу: 
```text
http://127.0.0.1/api/post/
```
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
