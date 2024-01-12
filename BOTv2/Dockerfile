# Используем базовый образ с поддержкой Python
FROM python:3.10

# Добовляем поддержку RU lacale
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Копируем файлы в рабочую директорию
WORKDIR /app
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Запускаем приложение
CMD ["python3", "start_bot.py"]
