FROM python:3.10

# Evita cache e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Executa sequência completa: migrações, popular dados, criar admin e iniciar servidor
CMD sh -c "\
    python manage.py makemigrations && \
    python manage.py migrate --noinput && \
    python3 utils/requirements.py && \
    python3 utils/fake.py && \
    python manage.py shell -c 'from django.contrib.auth import get_user_model; \
User=get_user_model(); \
User.objects.filter(username=\"user\").exists() or \
User.objects.create_superuser(\"user\", \"user@example.com\", \"123456\")' && \
    python manage.py runserver 0.0.0.0:8000"
