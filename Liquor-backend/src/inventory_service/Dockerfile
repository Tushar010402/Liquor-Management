FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=inventory_service.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ./src/inventory_service /app/

# Run migrations and collect static files at build time
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8002

# Run gunicorn
CMD ["gunicorn", "inventory_service.wsgi:application", "--bind", "0.0.0.0:8002"]