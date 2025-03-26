#!/bin/bash

# Liquor Management System Test Verification Script
# This script runs the tests that have been implemented but not verified

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Liquor Management System Test Verification Script"
    echo ""
    echo "Usage: ./run_verification_tests.sh [options]"
    echo ""
    echo "Options:"
    echo "  --all                Run all unverified tests"
    echo "  --e2e                Run unverified E2E tests"
    echo "  --performance        Run unverified performance tests"
    echo "  --security           Run unverified security tests"
    echo "  --module MODULE      Run tests for a specific module"
    echo "  --verbose, -v        Enable verbose output"
    echo "  --help, -h           Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_verification_tests.sh --e2e"
    echo "  ./run_verification_tests.sh --module inventory_flow"
    echo "  ./run_verification_tests.sh --all --verbose"
}

# Function to run tests and display results
run_test() {
    local module=$1
    local category=$2
    local verbose=$3
    
    echo -e "${YELLOW}Running tests for $module...${NC}"
    
    # Build the command
    CMD="python run_tests.py --category $category --module $module"
    
    if [ "$verbose" = true ]; then
        CMD="$CMD --verbose"
    fi
    
    # Run the tests
    echo "Command: $CMD"
    if $CMD; then
        echo -e "${GREEN}✅ Tests for $module passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Tests for $module failed!${NC}"
        return 1
    fi
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

# Initialize counters
PASSED=0
FAILED=0
TOTAL=0

# Run tests based on the specified category or module
if [ -n "$MODULE" ]; then
    # Run tests for a specific module
    if run_test "$MODULE" "$(echo "$MODULE" | cut -d'_' -f2)" "$VERBOSE"; then
        PASSED=$((PASSED + 1))
    else
        FAILED=$((FAILED + 1))
    fi
    TOTAL=$((TOTAL + 1))
elif [ "$CATEGORY" = "all" ]; then
    # Run all unverified tests
    
    # E2E tests
    echo -e "\n${YELLOW}Running unverified E2E tests...${NC}"
    for module in inventory_flow purchase_flow accounting_flow reporting_flow; do
        if run_test "$module" "e2e" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
    
    # Performance tests
    echo -e "\n${YELLOW}Running unverified performance tests...${NC}"
    for module in database_load kafka_throughput; do
        if run_test "$module" "performance" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
    
    # Security tests
    echo -e "\n${YELLOW}Running unverified security tests...${NC}"
    for module in api_security data_security; do
        if run_test "$module" "security" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
elif [ "$CATEGORY" = "e2e" ]; then
    # Run unverified E2E tests
    echo -e "\n${YELLOW}Running unverified E2E tests...${NC}"
    for module in inventory_flow purchase_flow accounting_flow reporting_flow; do
        if run_test "$module" "e2e" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
elif [ "$CATEGORY" = "performance" ]; then
    # Run unverified performance tests
    echo -e "\n${YELLOW}Running unverified performance tests...${NC}"
    for module in database_load kafka_throughput; do
        if run_test "$module" "performance" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
elif [ "$CATEGORY" = "security" ]; then
    # Run unverified security tests
    echo -e "\n${YELLOW}Running unverified security tests...${NC}"
    for module in api_security data_security; do
        if run_test "$module" "security" "$VERBOSE"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
fi

# Print summary
echo -e "\n${YELLOW}Test Summary:${NC}"
echo -e "Total: $TOTAL, Passed: ${GREEN}$PASSED${NC}, Failed: ${RED}$FAILED${NC}"

# Exit with appropriate status code
if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed!${NC}"
    exit 1
fi
