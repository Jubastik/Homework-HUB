# Используем базовый образ с поддержкой Python
FROM python:3.10

# Копируем файлы в рабочую директорию
WORKDIR /app
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Запускаем приложение
CMD ["python3", "."]
