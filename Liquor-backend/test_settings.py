"""
Django settings for testing.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-test-key-for-testing-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    # Auth service apps
    'auth_service.authentication.apps.AuthenticationConfig',
    'auth_service.roles.apps.RolesConfig',
    'auth_service.tenants.apps.TenantsConfig',
    'auth_service.users.apps.UsersConfig',
    'auth_service.shops.apps.ShopsConfig',
    'auth_service.common.apps.CommonConfig',
    
    # Core service apps
    'core_service.tenants.apps.TenantsConfig',
    'core_service.shops.apps.ShopsConfig',
    'core_service.settings.apps.SettingsConfig',
    'core_service.common.apps.CommonConfig',
    
    # Inventory service apps
    'inventory_service.brands.apps.BrandsConfig',
    'inventory_service.products.apps.ProductsConfig',
    'inventory_service.stock.apps.StockConfig',
    'inventory_service.suppliers.apps.SuppliersConfig',
    'inventory_service.common.apps.CommonConfig',
    
    # Purchase service apps
    'purchase_service.purchase_orders.apps.PurchaseOrdersConfig',
    'purchase_service.goods_receipt.apps.GoodsReceiptConfig',
    'purchase_service.suppliers.apps.SuppliersConfig',
    'purchase_service.common.apps.CommonConfig',
    
    # Sales service apps
    'sales_service.sales.apps.SalesConfig',
    'sales_service.approvals.apps.ApprovalsConfig',
    'sales_service.returns.apps.ReturnsConfig',
    'sales_service.cash.apps.CashConfig',
    'sales_service.common.apps.CommonConfig',
    
    # Accounting service apps
    'accounting_service.accounts.apps.AccountsConfig',
    'accounting_service.journals.apps.JournalsConfig',
    'accounting_service.ledger.apps.LedgerConfig',
    'accounting_service.reports.apps.ReportsConfig',
    'accounting_service.common.apps.CommonConfig',
    
    # Reporting service apps
    'reporting_service.common.apps.CommonConfig',
    
    # Common app
    'common.apps.CommonConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# JWT settings
JWT_SECRET_KEY = 'test-jwt-secret-key'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 3600  # 1 hour

# Auth service URL
AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:8000')
