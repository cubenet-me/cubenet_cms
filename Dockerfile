# Используем официальный Python 3.12 slim образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Добавляем /app в PYTHONPATH, чтобы импорты работали
ENV PYTHONPATH=/app

# Копируем проект в контейнер
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Экспортируем порт
EXPOSE 8585

# Запуск приложения через Uvicorn
CMD ["uvicorn", "engine.main:app", "--reload", "--host", "0.0.0.0", "--port", "8585"]
