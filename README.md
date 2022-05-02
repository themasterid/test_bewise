![foodgram-project-react Workflow Status](https://github.com/themasterid/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)
# Тестовое задание bewise

Задание доступно по адресу http://62.84.115.143/api/post

## Описание задания bewise
- В сервисе реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer}.
- После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
- Далее, полученные ответы сохраняются в базе данных из п. 1, причем сохраняется как минимум следующая информация: ID вопроса, Текст вопроса, Текст ответа, Дата создания вопроса.
- Если в БД имеется такой же вопрос, к публичному API с викторинами выполняются дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
- Ответом на запрос из п.2.a предыдущей сохранённый вопрос для викторины.В случае его отсутствия - пустой объект.


## Запуск с использованием CI/CD

Установить docker, docker-compose на сервере виртуальной машины Yandex.Cloud:
```bash
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Создаем папку infra:
```bash
mkdir infra
```
- Переносим файлы docker-compose.yml и default.conf на сервер.

```bash
scp docker-compose.yml username@server_ip:/home/username/
scp default.conf username@server_ip:/home/username/
```
- Создайте файл .env в дериктории infra, позже в него будем добавлять данные с git secrets:

```bash
touch .env
```
- Заполнить в настройках репозитория секреты .env

```python
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT='5432'
SECRET_KEY=
ALLOWED_HOSTS=
```

## Запуск проекта через Docker
- В папке infra выполнить команду, что бы собрать контейнер:
```bash
sudo docker-compose up -d
```

Для доступа к контейнеру выполните следующие команды:

```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение

```bash
source /venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Выполнить миграции:

```bash
python manage.py migrate
```

- В папке с файлом manage.py выполнить команду:
```bash
python manage.py runserver
```

### Документация к API доступна после запуска
```url
http://127.0.0.1/api/post/
```