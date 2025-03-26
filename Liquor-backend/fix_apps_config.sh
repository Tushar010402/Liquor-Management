#!/bin/bash

# Exit on error
set -e

echo "=== Fixing Django App Configurations ==="

# Fix core_service apps
echo "Fixing core_service apps.py files..."
for app in tenants shops settings common; do
    app_dir="src/core_service/${app}"
    if [ -d "$app_dir" ]; then
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_service.${app}'
    
    def ready(self):
        import core_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix inventory_service apps
echo "Fixing inventory_service apps.py files..."
for app in brands products suppliers stock common; do
    app_dir="src/inventory_service/${app}"
    if [ -d "$app_dir" ]; then
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_service.${app}'
    
    def ready(self):
        import inventory_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix auth_service apps
echo "Fixing auth_service apps.py files..."
for app in authentication common; do
    app_dir="src/auth_service/${app}"
    if [ -d "$app_dir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$app_dir"
        # Ensure __init__.py exists
        touch "$app_dir/__init__.py"
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service.${app}'
    
    def ready(self):
        import auth_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix sales_service apps
echo "Fixing sales_service apps.py files..."
for app in common; do
    app_dir="src/sales_service/${app}"
    if [ -d "$app_dir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$app_dir"
        # Ensure __init__.py exists
        touch "$app_dir/__init__.py"
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.${app}'
    
    def ready(self):
        import sales_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix purchase_service apps
echo "Fixing purchase_service apps.py files..."
for app in common; do
    app_dir="src/purchase_service/${app}"
    if [ -d "$app_dir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$app_dir"
        # Ensure __init__.py exists
        touch "$app_dir/__init__.py"
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_service.${app}'
    
    def ready(self):
        import purchase_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix reporting_service apps
echo "Fixing reporting_service apps.py files..."
for app in common; do
    app_dir="src/reporting_service/${app}"
    if [ -d "$app_dir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$app_dir"
        # Ensure __init__.py exists
        touch "$app_dir/__init__.py"
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reporting_service.${app}'
    
    def ready(self):
        import reporting_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Fix accounting_service apps
echo "Fixing accounting_service apps.py files..."
for app in common; do
    app_dir="src/accounting_service/${app}"
    if [ -d "$app_dir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$app_dir"
        # Ensure __init__.py exists
        touch "$app_dir/__init__.py"
        # Ensure apps.py exists and has correct configuration
        cat > "$app_dir/apps.py" << EOF
from django.apps import AppConfig


class $(echo "${app^}")Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.${app}'
    
    def ready(self):
        import accounting_service.${app}.signals
EOF
        # Ensure signals.py exists
        if [ ! -f "$app_dir/signals.py" ]; then
            echo "Creating signals.py for $app_dir"
            cat > "$app_dir/signals.py" << EOF
# Signal handlers for $(echo ${app}) app
EOF
        fi
    fi
done

# Update all __init__.py to ensure they're not empty
find src -name __init__.py -type f -exec touch {} \;

echo "=== App configuration fixes completed ===" 