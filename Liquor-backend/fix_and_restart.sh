#!/bin/bash

set -e

echo "=== Liquor Management System Fix and Restart ==="

# Make the script executable
chmod +x fix_apps_config.sh
chmod +x docker-entrypoint.sh

# Stop and remove all containers
echo "Stopping existing Docker services..."
sudo docker-compose down -v

# Copy the docker-entrypoint.sh to all service directories
echo "Ensuring all services have the updated entrypoint..."
for service in auth_service core_service sales_service inventory_service purchase_service reporting_service accounting_service; do
    cp docker-entrypoint.sh src/$service/docker-entrypoint.sh
    chmod +x src/$service/docker-entrypoint.sh
done

# Run the fix script locally to ensure all service modules are correctly structured
echo "Running app configuration fixes..."
./fix_apps_config.sh

# Create __init__.py files in all directories
echo "Creating Python package structure..."
find src -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# Set proper permissions for log directories
echo "Setting permissions for log directories..."
mkdir -p src/auth_service/logs
mkdir -p src/core_service/logs
mkdir -p src/sales_service/logs
mkdir -p src/inventory_service/logs
mkdir -p src/purchase_service/logs
mkdir -p src/reporting_service/logs
mkdir -p src/accounting_service/logs
sudo chmod -R 777 src/*/logs

# Build and start Docker services with clean configuration
echo "Building and starting Docker services..."
sudo docker-compose build --no-cache
sudo docker-compose up -d

echo "=== Services restarted, check logs with 'docker-compose logs -f' ===" 