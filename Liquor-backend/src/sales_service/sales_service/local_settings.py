"""
Local development settings for sales_service project.
"""

from .settings import *

# Local development settings
DEBUG = True
SECRET_KEY = 'django-insecure-key-for-dev-only'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Use local memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Service URLs
AUTH_SERVICE_URL = 'http://localhost:8000'
CORE_SERVICE_URL = 'http://localhost:8001'
INVENTORY_SERVICE_URL = 'http://localhost:8003'
PURCHASE_SERVICE_URL = 'http://localhost:8004'
REPORTING_SERVICE_URL = 'http://localhost:8005'
ACCOUNTING_SERVICE_URL = 'http://localhost:8006'

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092' 