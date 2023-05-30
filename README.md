# Latest News

  ![latest_news_workflow](https://github.com/AbbadonAA/Latest_News_Bot/workflows/latest_news_workflow/badge.svg)

 ## Описание 
  
 **Latest News** - это API сервиса для парсинга новостных статей с интегрированным ботом Telegram.

 API может быть использован для взаимодействия со сторонними ботами Telegram или иными сервисами - новостными агрегаторами.

 **Основной функционал API:**
 - Запуск парсеров для заполнения БД новостными статьями;
 - Очистка БД от устаревших новостных статей;
 - Управление пользователями: регистрация, аутентификация, авторизация, редактирование;
 - Получение из БД записей с новостными статьями с возможностью фильтрации. Полученные пользователем статьи помечаются прочитанными и исключаются из ответа при следующих запросах;
 - Формирование html-шаблона статьи для корректного отображения при помощи InstantView Telegram.

 **Реализован парсинг следующих новостных ресурсов:**
 - РБК;
 - ИноСМИ.
  
 **Настроены:** 
 - Автоматическое создание первого суперпользователя при запуске проекта;
 - CI/CD (GitHub Actions + Docker-Compose).
  
 ## Ключевые технологии и библиотеки: 
 [![Python][Python-badge]][Python-url]
 [![FastAPI][FastAPI-badge]][FastAPI-url]
 [![Scrapy][Scrapy-badge]][Scrapy-url]
 [![Python-telegram-bot][Python-telegram-bot-badge]][Python-telegram-bot-url]
 [![Postgres][Postgres-badge]][Postgres-url]
 [![SQLAlchemy][SQLAlchemy-badge]][SQLAlchemy-url]
 [![Docker][Docker-badge]][Docker-url]
 [![Nginx][Nginx-badge]][Nginx-url]

 ## Полная установка для локального запуска
 1. Склонируйте репозиторий: 
 ```shell
 git clone git@github.com:AbbadonAA/Latest_News_Bot.git
 ``` 
 2. Активируйте venv и установите зависимости: 
 ```shell
 python3 -m venv venv 
 source venv/bin/activate 
 pip install -r requirements.txt 
 ``` 
 3. Создайте в корневой директории файл .env со следующим наполнением: 
 ```dotenv
# Переменные API
APP_TITLE=LATEST_NEWS_PARSER  # (пример) название приложения
DEBUG=False  # True для включения режима отладки
HOST=0.0.0.0  # хост
PORT=8080  # порт
DOMAIN=False  # имеется ли DOMAIN_NAME
DOMAIN_NAME=https://example.com  # пример при наличии (необходим сертификат SSL)
PARSER_FREQUENCY=5  # периодичность запуска парсеров (минуты)
STORAGE_DAYS=30  # срок хранения данных в БД
SECRET=539e2390-9cc3-4bc7-aec1-2e96471ba49f  # (пример) uuid для хеширования
FIRST_SUPERUSER_EMAIL=admin@gmail.com  # (пример) email первого суперпользователя
FIRST_SUPERUSER_PASSWORD=AdmiN_123456789  # (пример) пароль суперпользователя

# Переменные бота
IP=127.0.0.1  # (пример) адрес вашего сервера
WEBHOOK=False # True для запуска бота в режиме webhook
BOT_TOKEN=5157247582:ATFpZanqlutiNMJfvO6tiNUDPnBkFAmiVi4  # (пример) токен бота Telegram

# Переменные базы данных
POSTGRES_DB=news_db  # название БД
POSTGRES_USER=postgres  # имя пользователя БД
POSTGRES_PASSWORD=postgres  # пароль БД
DB_HOST=localhost  # хост БД (для запуска через docker-compose заменить на имя сервиса с БД)
DB_PORT=7000  # порт БД
 ``` 

> **Warning**:
> Для локального запуска рекомендуется не указывать домен (DOMAIN=False) и запускать бота в режиме polling (WEBHOOK=False). В случае запуска бота в режиме webhook требуется наличие доменного имени с установленным сертификатом SSL. Иначе потребуется использовать Ngrok.

<details>
<summary><b><i>Использование Ngrok</i></b></summary>

----

Ngrok позволяет создавать временный
общедоступный адрес (туннель) локального сервера.

Подробнее: https://ngrok.com/

  - Установите Ngrok, следуя официальным инструкциям:

    https://ngrok.com/download

  - Запустите Ngrok и введите команду:
      ```shell
      ngrok http 8080
      ```
  - Задайте значение переменной окружения (.env):
      ```dotenv
      DOMAIN_NAME=https://1234-56-78-9.eu.ngrok.io  # Пример
      ```
----
</details>

 4. Запустите контейнер с базой данных PostgreSQL (должен быть установлен Docker): 
 ```shell
 cd infra/
 docker-compose -f docker-compose.local.yml up news_db -d
 ``` 
 5. В корневой директории примените миграции для создания таблиц в БД: 
 ```shell
 alembic upgrade head 
 ``` 
 6. Проект готов к запуску. 

 ## Управление при локальном запуске: 
 В корневой директории выполните команду: 
 ```shell
 python run.py
 ``` 
 Сервис будет запущен и доступен по следующим адресам:

 *(при условии, что в файле .env: HOST=0.0.0.0, PORT=8080)*
 - http://127.0.0.1:8080 - API 
 - http://127.0.0.1:8080/docs - документация Swagger
 - http://127.0.0.1:8080/redoc - документация ReDoc 
  
 Также будет запущен бот Telegram, токен которого указан в файле .env.

 В БД будет автоматически создан первый суперпользователь (email, password указаны в файле .env).

<details>
<summary><b><i>Упрощенный вариант установки для запуска в контейнерах</i></b></summary>

1. Создайте директорию для приложения: 
 ```shell
 mkdir LATEST_NEWS (пример)
 ``` 
2. Разместите в созданной директории файл .env со следующим наполнением:
```dotenv
# Переменные API
APP_TITLE=LATEST_NEWS_PARSER  # (пример) название приложения
DEBUG=False  # True для включения режима отладки
HOST=0.0.0.0  # хост
PORT=8080  # порт
DOMAIN=False  # имеется ли DOMAIN_NAME
DOMAIN_NAME=https://example.com  # пример при наличии (необходим сертификат SSL)
PARSER_FREQUENCY=5  # периодичность запуска парсеров (минуты)
STORAGE_DAYS=30  # срок хранения данных в БД
SECRET=539e2390-9cc3-4bc7-aec1-2e96471ba49f  # (пример) uuid для хеширования
FIRST_SUPERUSER_EMAIL=admin@gmail.com  # (пример) email первого суперпользователя
FIRST_SUPERUSER_PASSWORD=AdmiN_123456789  # (пример) пароль суперпользователя

# Переменные бота
IP=127.0.0.1  # (пример) адрес вашего сервера
WEBHOOK=False # True для запуска бота в режиме webhook
BOT_TOKEN=5157247582:ATFpZanqlutiNMJfvO6tiNUDPnBkFAmiVi4  # (пример) токен бота Telegram

# Переменные базы данных
POSTGRES_DB=news_db  # название БД
POSTGRES_USER=postgres  # имя пользователя БД
POSTGRES_PASSWORD=postgres  # пароль БД
DB_HOST=news_db  # хост БД
DB_PORT=7000  # порт БД
 ``` 
3. В директории приложения создайте директорию /infra:
```shell
mkdir infra
```
4. Разместите в директории /infra файл docker-compose.local.yml
5. В директории /infra запустите docker-compose:
```shell
docker-compose -f docker-compose.local.yml up -d
```
6. Проект запущен в двух контейнерах:
- latest_news_bot
- latest_news_db
</details>

 ## Установка на сервере и получение сертификата SSL
1. Создайте на сервере директорию для приложения: 
 ```shell
 mkdir latest-news (пример) 
 ``` 
2. Разместите в созданной директории файл .env со следующим наполнением:
```dotenv
# Переменные API
APP_TITLE=LATEST_NEWS_PARSER  # (пример) название приложения
DEBUG=False  # True для включения режима отладки
HOST=0.0.0.0  # хост
PORT=8080  # порт
DOMAIN=True  # имеется ли DOMAIN_NAME
DOMAIN_NAME=https://example.com  # (пример)
PARSER_FREQUENCY=5  # периодичность запуска парсеров (минуты)
STORAGE_DAYS=30  # срок хранения данных в БД
SECRET=539e2390-9cc3-4bc7-aec1-2e96471ba49f  # (пример) uuid для хеширования
FIRST_SUPERUSER_EMAIL=admin@gmail.com  # (пример) email первого суперпользователя
FIRST_SUPERUSER_PASSWORD=AdmiN_123456789  # (пример) пароль суперпользователя

# Переменные бота
IP=127.0.0.1  # (пример) адрес вашего сервера
WEBHOOK=True # Запуск бота в режиме webhook
BOT_TOKEN=5157247582:ATFpZanqlutiNMJfvO6tiNUDPnBkFAmiVi4  # (пример) токен бота Telegram

# Переменные базы данных
POSTGRES_DB=news_db  # название БД
POSTGRES_USER=postgres  # имя пользователя БД
POSTGRES_PASSWORD=postgres  # пароль БД
DB_HOST=news_db  # хост БД
DB_PORT=7000  # порт БД
 ```
3. Создайте директорию /infra:
```shell
mkdir infra
```
4. Разместите в директории /infra файл docker-compose.prod.yml
5. Уточните в файле docker-compose.prod.yml переменные окружения:
```dotenv
VIRTUAL_HOST=example.com (укажите Ваш домен)
LETSENCRYPT_HOST=example.com (укажите Ваш домен)
LETSENCRYPT_EMAIL=your_email@example.com (укажите Ваш email)
```
6. Разместите в директории /infra файл docker-compose.nginx.yml
7. Создайте сеть Docker:
```shell
docker network create nginx-proxy
```
8. Запустите контейнеры:
```shell
docker-compose -f docker-compose.nginx.yml up -d
docker-compose -f docker-compose.prod.yml up -d
```
9. Проект запущен в четырех контейнерах:
- latest_news_bot
- latest_news_db
- nginx-proxy
- letsencrypt

  Получен сертификат SSL и настроено автоматическое обновление сертификатов.

 ## Лицензия 
 - ### **MIT License** 
  
 ### Автор 
 Pushkarev Anton 
  
 pushkarevantona@gmail.com

 <!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/
[Python-badge]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white

[FastAPI-url]: https://fastapi.tiangolo.com/
[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[Scrapy-url]: https://pypi.org/project/Scrapy/
[Scrapy-badge]: https://img.shields.io/badge/-Scrapy-forestgreen?style=for-the-badge&

[Python-telegram-bot-url]: https://github.com/python-telegram-bot/python-telegram-bot
[Python-telegram-bot-badge]: https://img.shields.io/badge/python--telegram--bot-2CA5E0?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/
[Postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[SQLAlchemy-url]: https://pypi.org/project/SQLAlchemy/
[SQLAlchemy-badge]: https://img.shields.io/badge/-SQLAlchemy-dimgrey?style=for-the-badge&

[Docker-url]: https://www.docker.com/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[Nginx-url]: https://nginx.org
[Nginx-badge]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white~~
