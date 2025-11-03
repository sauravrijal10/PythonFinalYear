FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required system packages for MySQL
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config build-essential netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Wait for the database to be ready before running migrations
COPY ./wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Start the app
CMD ["sh", "-c", "/wait-for-db.sh && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
