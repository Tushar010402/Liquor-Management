#!/bin/bash

# Script to install the required dependencies for the Liquor Management System tests

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Liquor Management System Dependencies Installer"
    echo ""
    echo "Usage: ./install_dependencies.sh [options]"
    echo ""
    echo "Options:"
    echo "  --help, -h           Show this help message"
    echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    python -m venv venv
    source venv/bin/activate
fi

# Install dependencies for each service
echo "Installing Auth Service dependencies..."
pip install -r src/auth_service/requirements.txt

echo "Installing Core Service dependencies..."
pip install -r src/core_service/requirements.txt

echo "Installing Sales Service dependencies..."
pip install -r src/sales_service/requirements.txt

echo "All dependencies installed successfully!"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"

# Install pytest and related packages
echo -e "${YELLOW}Installing pytest and related packages...${NC}"
pip install pytest pytest-django pytest-mock pytest-cov

# Install Django and related packages
echo -e "${YELLOW}Installing Django and related packages...${NC}"
pip install django djangorestframework django-cors-headers django-filter

# Install Kafka packages
echo -e "${YELLOW}Installing Kafka packages...${NC}"
pip install confluent-kafka

# Install JWT packages
echo -e "${YELLOW}Installing JWT packages...${NC}"
pip install pyjwt

# Install database packages
echo -e "${YELLOW}Installing database packages...${NC}"
pip install psycopg2-binary

# Install other packages
echo -e "${YELLOW}Installing other packages...${NC}"
pip install requests

# Install development packages
echo -e "${YELLOW}Installing development packages...${NC}"
pip install black isort flake8

# Install packages from requirements files
for req_file in $(find . -name "requirements.txt"); do
    echo -e "${YELLOW}Installing packages from $req_file...${NC}"
    pip install -r $req_file
done

# Print installed packages
echo -e "${YELLOW}Installed packages:${NC}"
pip list

# Deactivate virtual environment
echo -e "${YELLOW}Deactivating virtual environment...${NC}"
deactivate

echo -e "${GREEN}Dependencies installed successfully!${NC}"
