#!/bin/bash

# Function to wait for a service to be ready
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service to be ready..."
    while ! nc -z $host $port; do
        if [ $attempt -eq $max_attempts ]; then
            echo "Error: $service is not ready after $max_attempts attempts"
            exit 1
        fi
        echo "Attempt $attempt/$max_attempts: $service is not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "$service is ready!"
}

# Ensure pkg_resources is available
if ! python -c "import pkg_resources" 2>/dev/null; then
    echo "Installing setuptools to ensure pkg_resources is available..."
    pip install --no-cache-dir setuptools==69.1.0
fi

# Wait for dependencies
wait_for_service postgres 5432 "PostgreSQL"
wait_for_service redis 6379 "Redis"
wait_for_service kafka 29092 "Kafka"

# Create __init__.py files in all directories
echo "Creating __init__.py files in all directories..."
find /app/src -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# Fix missing app modules before proceeding
echo "Fixing app configurations..."

# Function to fix app configuration for a service
fix_app_config() {
    local service_name=$1
    local app_name=$2
    local app_dir="/app/src/${service_name}/${app_name}"
    
    mkdir -p "$app_dir"
    touch "$app_dir/__init__.py"
    
    # Create apps.py with correct configuration
    cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app_name^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '${service_name}.${app_name}'
    
    def ready(self):
        import ${service_name}.${app_name}.signals
EOF
    
    # Create signals.py if it doesn't exist
    if [ ! -f "$app_dir/signals.py" ]; then
        cat > "$app_dir/signals.py" << EOF
# Signal handlers for ${app_name} app
EOF
    fi
}

# Fix missing modules for each service
fix_app_config "core_service" "tenants"
fix_app_config "core_service" "shops"
fix_app_config "core_service" "settings"
fix_app_config "core_service" "common"

fix_app_config "inventory_service" "brands"
fix_app_config "inventory_service" "products"
fix_app_config "inventory_service" "suppliers"
fix_app_config "inventory_service" "stock"
fix_app_config "inventory_service" "common"

fix_app_config "auth_service" "authentication"
fix_app_config "auth_service" "common"

fix_app_config "sales_service" "common"
fix_app_config "purchase_service" "common"
fix_app_config "reporting_service" "common"
fix_app_config "accounting_service" "common"

# Set PYTHONPATH
export PYTHONPATH=/app

# Change to the service directory
case $SERVICE_NAME in
    "auth")
        cd /app/src/auth_service
        ;;
    "core")
        cd /app/src/core_service
        ;;
    "sales")
        cd /app/src/sales_service
        ;;
    "inventory")
        cd /app/src/inventory_service
        ;;
    "purchase")
        cd /app/src/purchase_service
        ;;
    "reporting")
        cd /app/src/reporting_service
        ;;
    "accounting")
        cd /app/src/accounting_service
        ;;
    *)
        echo "Unknown service: $SERVICE_NAME"
        exit 1
        ;;
esac

# Run migrations and collect static files for the service
python manage.py migrate
python manage.py collectstatic --noinput

# Start the appropriate service
case $SERVICE_NAME in
    "auth")
        python manage.py runserver 0.0.0.0:8000
        ;;
    "core")
        python manage.py runserver 0.0.0.0:8001
        ;;
    "sales")
        python manage.py runserver 0.0.0.0:8002
        ;;
    "inventory")
        python manage.py runserver 0.0.0.0:8003
        ;;
    "purchase")
        python manage.py runserver 0.0.0.0:8004
        ;;
    "reporting")
        python manage.py runserver 0.0.0.0:8005
        ;;
    "accounting")
        python manage.py runserver 0.0.0.0:8006
        ;;
    *)
        echo "Unknown service: $SERVICE_NAME"
        exit 1
        ;;
esac 