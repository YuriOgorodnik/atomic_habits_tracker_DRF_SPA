# Устанавливаем базовый образ из репозитория Python версии 3.11
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера как /app
WORKDIR /app

# Копируем файл requirements.txt из локальной директории внутрь контейнера в /app/
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt внутри контейнера
RUN pip install -r requirements.txt

# Копируем все файлы из текущей локальной директории внутрь контейнера в /app/
COPY . /app/