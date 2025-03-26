#!/bin/bash

# Liquor Management System Test Runner Script
# This script provides a convenient way to run tests for the Liquor Management System

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Function to display help
show_help() {
    echo "Liquor Management System Test Runner"
    echo ""
    echo "Usage: ./run_tests.sh [options]"
    echo ""
    echo "Options:"
    echo "  --all                Run all tests"
    echo "  --unit               Run unit tests"
    echo "  --integration        Run integration tests"
    echo "  --e2e                Run end-to-end tests"
    echo "  --performance        Run performance tests"
    echo "  --security           Run security tests"
    echo "  --service SERVICE    Run tests for a specific service"
    echo "                       (auth, core, inventory, purchase, sales, accounting, reporting)"
    echo "  --module MODULE      Run tests for a specific module"
    echo "  --verbose, -v        Enable verbose output"
    echo "  --coverage           Generate coverage report"
    echo "  --help, -h           Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh --integration"
    echo "  ./run_tests.sh --e2e --verbose"
    echo "  ./run_tests.sh --service inventory --verbose"
    echo "  ./run_tests.sh --all --coverage"
}

# Parse command line arguments
CATEGORY=""
SERVICE=""
MODULE=""
VERBOSE=""
COVERAGE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            CATEGORY="all"
            shift
            ;;
        --unit)
            CATEGORY="unit"
            shift
            ;;
        --integration)
            CATEGORY="integration"
            shift
            ;;
        --e2e)
            CATEGORY="e2e"
            shift
            ;;
        --performance)
            CATEGORY="performance"
            shift
            ;;
        --security)
            CATEGORY="security"
            shift
            ;;
        --service)
            SERVICE="$2"
            shift 2
            ;;
        --module)
            MODULE="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            shift
            ;;
        --coverage)
            COVERAGE="--coverage"
            shift
            ;;
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

# Build the command
CMD="python run_tests.py"

if [ -n "$CATEGORY" ]; then
    CMD="$CMD --category $CATEGORY"
fi

if [ -n "$SERVICE" ]; then
    CMD="$CMD --service $SERVICE"
fi

if [ -n "$MODULE" ]; then
    CMD="$CMD --module $MODULE"
fi

if [ -n "$VERBOSE" ]; then
    CMD="$CMD $VERBOSE"
fi

if [ -n "$COVERAGE" ]; then
    CMD="$CMD $COVERAGE"
fi

# Run the tests
echo "Running tests with command: $CMD"
$CMD

# Deactivate virtual environment
deactivate
