# Liquor Management System Test Setup

This document provides instructions on how to set up and run the tests for the Liquor Management System backend.

## Overview

The Liquor Management System backend tests are organized into several categories:

1. **Unit Tests**: Tests for individual components in isolation.
2. **Integration Tests**: Tests for the interaction between different services.
3. **End-to-End (E2E) Tests**: Tests for complete business flows across multiple services.
4. **Performance Tests**: Tests for the system's ability to handle expected load.
5. **Security Tests**: Tests for the system's security mechanisms.

## Setup Instructions

### 1. Fix Python Path

The first step is to fix the Python path to ensure that the tests can find the modules in the src directory. Run the following command:

```bash
cd Liquor-backend
python fix_python_path.py
```

This script will:
- Add the src directory to the Python path in the pytest.ini file
- Add the src directory to the Python path in the run_tests.py script
- Create a pyproject.toml file to configure pytest
- Create a conftest.py file in the root directory to add the src directory to the Python path

### 2. Install Dependencies

The next step is to install the required dependencies in the virtual environment. Run the following command:

```bash
cd Liquor-backend
./install_dependencies.sh
```

This script will:
- Create a virtual environment if it doesn't exist
- Activate the virtual environment
- Install pytest and related packages
- Install Django and related packages
- Install Kafka packages
- Install JWT packages
- Install database packages
- Install other required packages
- Install packages from requirements files

### 3. Run Tests

Once the setup is complete, you can run the tests using the run_fixed_tests.sh script. This script will:
- Activate the virtual environment
- Set up the environment variables
- Run the tests with the specified options
- Deactivate the virtual environment

#### Running All Tests

```bash
cd Liquor-backend
./run_fixed_tests.sh --all
```

#### Running Integration Tests

```bash
cd Liquor-backend
./run_fixed_tests.sh --integration
```

#### Running E2E Tests

```bash
cd Liquor-backend
./run_fixed_tests.sh --e2e
```

#### Running Performance Tests

```bash
cd Liquor-backend
./run_fixed_tests.sh --performance
```

#### Running Security Tests

```bash
cd Liquor-backend
./run_fixed_tests.sh --security
```

#### Running Tests for a Specific Module

```bash
cd Liquor-backend
./run_fixed_tests.sh --module inventory_flow
```

#### Running Tests with Verbose Output

```bash
cd Liquor-backend
./run_fixed_tests.sh --all --verbose
```

## Troubleshooting

### 1. Python Path Issues

If you encounter issues with the Python path, try running the fix_python_path.py script again:

```bash
cd Liquor-backend
python fix_python_path.py
```

### 2. Missing Dependencies

If you encounter issues with missing dependencies, try running the install_dependencies.sh script again:

```bash
cd Liquor-backend
./install_dependencies.sh
```

### 3. Django Configuration Issues

If you encounter issues with Django configuration, check the test_settings.py file to ensure that all the required apps are included in the INSTALLED_APPS list.

### 4. Virtual Environment Issues

If you encounter issues with the virtual environment, try recreating it:

```bash
cd Liquor-backend
rm -rf venv
./install_dependencies.sh
```

## Test Results

The test results are summarized in the following files:

- TEST_RESULTS_SUMMARY.md: Summary of the test results
- TEST_FIX_PLAN.md: Plan to fix the issues found in the tests
- TEST_FIX_IMPLEMENTATION.md: Implementation of the fixes

## Next Steps

1. Run the tests to verify that the fixes have resolved the issues.
2. Update the test documentation to reflect the current status of the tests.
3. Set up a CI/CD pipeline for automated testing.
4. Implement load testing in a production-like environment.
5. Conduct penetration testing.
6. Implement continuous monitoring for performance and security.
