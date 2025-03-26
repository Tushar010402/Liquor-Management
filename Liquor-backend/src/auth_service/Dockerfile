FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=auth_service.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY src/auth_service/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
# Note: In development with docker-compose, this will be mounted as a volume
COPY src/auth_service/ /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Run gunicorn in production, development uses override in docker-compose
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]