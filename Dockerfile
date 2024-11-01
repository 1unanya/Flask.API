# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо файл requirements.txt
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли в робочий каталог
COPY . .

# Відкриваємо порт, який використовує ваш додаток
EXPOSE 5000

# Команда для запуску вашого додатку
CMD ["python", "apps.py"]
