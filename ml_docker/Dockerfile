FROM python:3.12-slim

WORKDIR /app

# Установка Nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

# Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Приложение и модель
COPY main.py .
COPY models/ ./models/

# HTML-страница
COPY frontend/ /var/www/html/

# Конфигурация Nginx
COPY nginx/default.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD ["sh", "-c", "uvicorn main:app --host 127.0.0.1 --port 5000 & nginx -g 'daemon off;'"]
