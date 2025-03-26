#!/bin/bash

# Script to run the tests with the fixed configuration

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Liquor Management System Test Runner with Fixed Configuration"
    echo ""
    echo "Usage: ./run_fixed_tests.sh [options]"
    echo ""
    echo "Options:"
    echo "  --all                Run all tests"
    echo "  --integration        Run integration tests"
    echo "  --e2e                Run E2E tests"
    echo "  --performance        Run performance tests"
    echo "  --security           Run security tests"
    echo "  --module MODULE      Run tests for a specific module"
    echo "  --verbose, -v        Enable verbose output"
    echo "  --help, -h           Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_fixed_tests.sh --e2e"
    echo "  ./run_fixed_tests.sh --module inventory_flow"
    echo "  ./run_fixed_tests.sh --all --verbose"
}

# Parse command line arguments
CATEGORY=""
MODULE=""
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            CATEGORY="all"
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
        --module)
            MODULE="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
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

# If no category or module is specified, show help
if [ -z "$CATEGORY" ] && [ -z "$MODULE" ]; then
    show_help
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Set up environment variables
echo -e "${YELLOW}Setting up environment variables...${NC}"
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export DJANGO_SETTINGS_MODULE=test_settings

# Build the command
CMD="python -m pytest"

if [ -n "$CATEGORY" ]; then
    if [ "$CATEGORY" = "all" ]; then
        CMD="$CMD src/"
    else
        CMD="$CMD src/${CATEGORY}_tests/"
    fi
elif [ -n "$MODULE" ]; then
    # Determine the category from the module name
    if [[ "$MODULE" == *"_flow" ]]; then
        CATEGORY="e2e"
    elif [[ "$MODULE" == *"_load" || "$MODULE" == *"_throughput" ]]; then
        CATEGORY="performance"
    elif [[ "$MODULE" == *"_security" ]]; then
        CATEGORY="security"
    else
        CATEGORY="integration"
    fi
    
    CMD="$CMD src/${CATEGORY}_tests/${MODULE}/"
fi

if [ "$VERBOSE" = true ]; then
    CMD="$CMD -v"
fi

# Run the tests
echo -e "${YELLOW}Running tests with command: $CMD${NC}"
$CMD

# Capture the exit code
EXIT_CODE=$?

# Deactivate virtual environment
echo -e "${YELLOW}Deactivating virtual environment...${NC}"
deactivate

# Exit with the same code as the tests
exit $EXIT_CODE
