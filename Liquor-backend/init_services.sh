#!/bin/bash

set -e

echo "=== Liquor Management System Initialization ==="

# Function to check and stop a process on a port
check_and_kill_process() {
    local port=$1
    local pid=$(sudo lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo "Process using port $port found with PID $pid, stopping it..."
        sudo kill -9 $pid
    fi
}

# Check and stop any processes using required ports
echo "Checking for processes using required ports..."
for port in 8000 8001 8002 8003 8004 8005 8006 5432 6379 2181 9092; do
    check_and_kill_process $port
done

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

# Make sure entrypoint script is executable
echo "Setting executable permissions for docker-entrypoint.sh..."
chmod +x docker-entrypoint.sh

# Run Docker services
echo "Stopping existing Docker services..."
sudo docker-compose down -v

echo "Building and starting Docker services..."
sudo docker-compose up --build

echo "=== Initialization complete ===" 