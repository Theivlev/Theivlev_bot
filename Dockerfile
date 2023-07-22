# Используйте базовый образ Python
FROM python:3.9

# Установите зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код вашего бота в контейнер
COPY . .


CMD ["python", "theivlevbot.py"]