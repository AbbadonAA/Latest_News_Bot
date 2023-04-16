# Latest News
  
 ## Описание 
  
 **Latest News** - это API сервиса для парсинга новостных статей с интегрированным ботом Telegram.

 API может быть использован для взаимодействия со сторонними ботами Telegram или как основа бэкенда для сайта - новостного агрегатора.

 Основной функционал API:
 - Запуск парсеров для заполнения БД новостными статьями;
 - Очистка БД от устаревших новостных статей;
 - Управление пользователями: регистрация, аутентификация, авторизация, редактирование;
 - Получение из БД записей с новостными статьями с возможностью фильтрации. Полученные пользователем статьи помечаются прочитанными и исключаются из ответа при следующих запросах;
 - Формирование html-шаблона статьи для корректного отображения при помощи InstantView Telegram.

 Реализован парсинг следующих новостных ресурсов:
 - РБК;
 - ИноСМИ.
  
 Настроены: 
 - Автоматическое создание первого суперпользователя при запуске проекта;
 - CI/CD (GitHub Actions + Docker-Compose).
  
 ## Ключевые технологии и библиотеки: 
 - [Python](https://www.python.org/); 
 - [FastAPI](https://fastapi.tiangolo.com/);
 - [Scrapy](https://pypi.org/project/Scrapy/);
 - [Python-Telegram-Bot](https://pypi.org/project/python-telegram-bot/);
 - [PostgreSQL](https://www.postgresql.org/);
 - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/); 
 - [Alembic](https://pypi.org/project/alembic/); 
 - [Pydantic](https://pypi.org/project/pydantic/); 
 - [Asyncio](https://docs.python.org/3/library/asyncio.html);
 - [Docker](https://www.docker.com/);
  
 ## Установка для локального запуска
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
APP_TITLE=  # название приложения
HOST=  # IP-адрес
PORT=  # порт
DOMAIN=False  # имеется ли доменное имя
DOMAIN_NAME=  # доменное имя (необходим сертификат SSL)
POSTGRES_DB=  # название БД
POSTGRES_USER=  # имя пользователя БД
POSTGRES_PASSWORD=  # пароль БД
DB_HOST=  # хост БД
DB_PORT=  # порт БД
DAYS=5  # срок хранения данных в БД
SECRET=  # любая последовательность символов для хеширования
FIRST_SUPERUSER_EMAIL=  # email первого суперпользователя
FIRST_SUPERUSER_PASSWORD=  # пароль суперпользователя
FIRST_SUPERUSER_CHAT_ID=  # chat_id суперпользователя
BOT_TOKEN=  # токен бота Telegram
 ``` 
 4. Запустите контейнер с базой данных PostgreSQL (должен быть установлен Docker): 
 ```shell
 cd infra/
 docker-compose up -d 
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

 *(при условии, что в файле .env: HOST=127.0.0.1, PORT=8080)*
 - http://127.0.0.1:8080 - API 
 - http://127.0.0.1:8080/docs - документация Swagger
 - http://127.0.0.1:8080/redoc - документация ReDoc 
  
 Также будет запущен бот Telegram, токен которого указан в файле .env.

 В БД будет автоматически создан первый суперпользователь (email, chat_id, password указаны в файле .env).

 ## Запуск сервиса на собственном сервере с использованием GitHub Actions
 1. Создайте директорию для приложения: 
 ```shell
 mkdir ... 
 ``` 
  
 ## Лицензия 
 - ### **MIT License** 
  
 ### Автор 
 Pushkarev Anton 
  
 pushkarevantona@gmail.com