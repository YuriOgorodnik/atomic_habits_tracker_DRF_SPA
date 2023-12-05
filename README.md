Atomic Habits App

Приложение "Atomic Habits" поможет вам управлять вашими важными для здоровья привычками, соблюдать регулярность их выполнения.

Описание проекта

Atomic Habits - это веб-приложение, которое помогает пользователям создавать, отслеживать и поддерживать полезные привычки. Приложение предоставляет возможность создавать привычки, устанавливать напоминания и отслеживать выполнение целей.

Стек технологий

Проект разработан с использованием следующего технологического стека:

    Python 3.11
    Django: веб-фреймворк для создания веб-приложений
    Django REST framework: библиотека для создания RESTful API
    Celery: для асинхронных задач
    Redis: как брокер сообщений для Celery

Инструкция по установке

Чтобы развернуть проект и начать его использовать необходимо выполнить следующие шаги:

    1. Склонируйте данный репозиторий: Выполните команду git clone для клонирования репозитория 
        на свой локальный компьютер.
    
    2. Установите все необходимые зависимости:
        
        cd atomic_habits
        pip install -r requirements.txt

    3. Настройте файл .env: Создайте файл .env в корневой директории проекта и добавьте в него переменные среды, 
        например:

        SECRET_KEY=your_secret_key

        POSTGRES_HOST=localhost
        POSTGRES_DB=your_database_name
        POSTGRES_USER=your_database
        POSTGRES_PASSWORD=your_database_password
        POSTGRES_PORT=5432

        ADMIN_PASSWORD=your_admin_password
        CHAT_ID_ADMIN=your_chat_id

        EMAIL_HOST_USER=your_email_address
        EMAIL_HOST_PASSWORD=your_email_password

        TELEGRAM_API_TOKEN=your_telegram_api_token
        CHAT_ID_USER=user_chat_id

        CELERY_BROKER_URL=redis://localhost:6379
        CELERY_RESULT_BACKEND=redis://localhost:6379

    4. Выполните миграции для создания базы данных:

        python manage.py makemigrations
        python manage.py migrate
    
    5. Для заполнения базы данных пользователями и имеющимися у них привычками запустите команду:

        python manage.py add_data_for_DB

    6. Для создания администратора запустите команду:

         python manage.py add_superuser

    7. Запустите приложение:

        python manage.py runserver

    8. Откройте приложение: перейдите в веб-браузере по адресу http://127.0.0.1:8000/ и начните 
        использовать приложение.

Краткое описание имеющихся эндпоинтов

В приложении "Atomic Habits" есть несколько важных эндпоинтов:

    /habits/ - список привычек.
    /habits/create/ - создание привычки.
    /habits/int:pk/ - просмотр привычки.
    /habits/update/<int:pk>/ - обновление привычки.
    /habits/delete/<int:pk>/ - удаление привычки.
    /habits/public/ - список публичных привычек.

    /users/ - список пользователей.
    /users/register/ - создание пользователя.
    /users/int:pk/ - просмотр пользователя.
    /users/update/<int:pk>/ - обновление пользователя.
    /users/delete/<int:pk>/ - удаление пользователя.


Если вы используете Celery на операционной системе Windows, то вам в команду запуска необходимо 
будет добавить: -P eventlet

Запустите Celery для асинхронной обработки задач, таких как отправка уведомлений:

    celery -A atomic_habits worker -l info -P eventlet
    celery -A atomic_habits beat

Для запуска проекта в Docker необходимо выполнить следующие шаги:

    1. Настройте файл .env: Создайте файл .env в корневой директории проекта и добавьте в него переменные среды, 
        например:

        SECRET_KEY=your_secret_key

        POSTGRES_HOST=db
        POSTGRES_DB=your_database_name
        POSTGRES_USER=your_database
        POSTGRES_PASSWORD=your_database_password
        POSTGRES_PORT=5432

        ADMIN_PASSWORD=your_admin_password
        CHAT_ID_ADMIN=your_chat_id

        EMAIL_HOST_USER=your_email_address
        EMAIL_HOST_PASSWORD=your_email_password

        TELEGRAM_API_TOKEN=your_telegram_api_token
        CHAT_ID_USER=user_chat_id

        CELERY_BROKER_URL=redis://redis:6379
        CELERY_RESULT_BACKEND=redis://redis:6379

    2. Для создания образа из Dockerfile и запуска контейнера запустите команду:

        docker-compose up --build 
        или
        docker-compose up -d --build (для запуска в фоновом режиме)

Автор проекта: Юрий Огородник

Документация проекта: http://127.0.0.1:8000/swagger/ или http://127.0.0.1:8000/redoc/