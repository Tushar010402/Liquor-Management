# Liquor Management System Testing Framework

This document provides an overview of the testing framework for the Liquor Management System backend. The system is built using a microservices architecture with multiple services communicating via Kafka events.

## Testing Strategy

The testing strategy follows a comprehensive approach, covering different levels of testing:

1. **Unit Tests**: Verify the functionality of individual components in isolation
2. **Integration Tests**: Verify the interaction between different services
3. **End-to-End (E2E) Tests**: Verify complete business flows across multiple services
4. **Performance Tests**: Verify the system's ability to handle expected load
5. **Security Tests**: Verify the system's security mechanisms

## Test Categories

### 1. Unit Tests

Unit tests verify the functionality of individual components in isolation. These tests are located in the `tests` directory of each service module.

Services covered:
- `auth_service`
- `core_service`
- `inventory_service`
- `purchase_service`
- `sales_service`
- `accounting_service`
- `reporting_service`

### 2. Integration Tests

Integration tests verify the interaction between different services, particularly focusing on event-based communication via Kafka.

Modules covered:
- `auth_inventory`: Tests the flow of user creation events from auth service to inventory service
- `auth_core`: Tests tenant and shop synchronization between auth and core services
- `inventory_sales`: Tests stock adjustment events between inventory and sales services
- `sales_accounting`: Tests financial transaction events between sales and accounting services
- `purchase_inventory`: Tests purchase order and goods receipt events between purchase and inventory services
- `inventory_reporting`: Tests stock level and expiry alert events between inventory and reporting services

### 3. End-to-End (E2E) Tests

E2E tests verify complete business flows across multiple services, simulating real user scenarios.

**Verified Modules:**
- `sales_flow`: Tests the complete sales creation and approval/rejection flows

**Implemented but Not Verified Modules:**
- `inventory_flow`: Tests the complete inventory management flow including stock adjustments
- `purchase_flow`: Tests the complete purchase order and goods receipt flow
- `accounting_flow`: Tests the complete accounting flow including sales transactions, purchase transactions, journal entries, and tax calculations
- `reporting_flow`: Tests the complete reporting flow including sales reports, inventory reports, financial reports, and dashboard data

### 4. Performance Tests

Performance tests verify the system's ability to handle expected load and stress conditions.

**Verified Modules:**
- `api_load`: Tests the sales API's performance under load using Locust

**Implemented but Not Verified Modules:**
- `database_load`: Tests database performance under load, including read operations, write operations, query performance, and transaction throughput
- `kafka_throughput`: Tests Kafka performance under load, including producer throughput, consumer throughput, message latency, and batch processing

### 5. Security Tests

Security tests verify the system's security mechanisms, including authentication, authorization, and data protection.

**Verified Modules:**
- `auth_security`: Tests JWT authentication and role-based access control

**Implemented but Not Verified Modules:**
- `api_security`: Tests API endpoint security, including authentication, authorization, input validation, rate limiting, and CSRF protection
- `data_security`: Tests data protection, including data encryption, data integrity, data privacy, data access controls, and data backup and recovery

## Test Implementation Details

### Mock Objects

The tests use mock objects to simulate external dependencies:
- `MockKafkaProducer`: Simulates Kafka message production
- `MockKafkaConsumer`: Simulates Kafka message consumption
- `MicroserviceUser`: Simulates authenticated users for testing

### Test Data

Test fixtures provide consistent test data for:
- Tenants
- Users
- Shops
- Brands
- Stock
- Sales
- Purchase orders

## Running Tests

### Using the Shell Script

The easiest way to run tests is using the `run_tests.sh` script:

```bash
# Run all tests
./run_tests.sh --all

# Run specific test categories
./run_tests.sh --integration
./run_tests.sh --e2e
./run_tests.sh --performance
./run_tests.sh --security

# Run tests for a specific service
./run_tests.sh --service inventory

# Run tests for a specific module
./run_tests.sh --module sales_flow

# Run tests with verbose output
./run_tests.sh --integration --verbose

# Generate coverage report
./run_tests.sh --all --coverage
```

### Using the Python Script

Alternatively, you can use the `run_tests.py` script directly:

```bash
# Run all tests
python run_tests.py --category all

# Run specific test categories
python run_tests.py --category integration
python run_tests.py --category e2e
python run_tests.py --category performance
python run_tests.py --category security

# Run tests for a specific service
python run_tests.py --service inventory

# Run tests for a specific module
python run_tests.py --module sales_flow

# Run tests with verbose output
python run_tests.py --category integration --verbose

# Generate JUnit XML reports
python run_tests.py --category all --junit-xml

# Generate coverage report
python run_tests.py --category all --coverage
```

### Using pytest Directly

You can also run tests using pytest directly:

```bash
# Run all tests
pytest src/

# Run specific test categories
pytest src/integration_tests/
pytest src/e2e_tests/
pytest src/performance_tests/
pytest src/security_tests/

# Run tests for a specific module
pytest src/e2e_tests/sales_flow/

# Run tests with verbose output
pytest -v src/integration_tests/

# Generate coverage report
pytest --cov=src/ --cov-report=html src/
```

## Test Reports

### JUnit XML Reports

JUnit XML reports are generated in the `test_reports` directory when running tests with the `--junit-xml` option.

### Coverage Reports

Coverage reports are generated in the `coverage_reports` directory when running tests with the `--coverage` option.

## Test Verification Status

| Category | Module | Status | Notes |
|----------|--------|--------|-------|
| Integration | auth_inventory | ✅ Verified | 1 test passed |
| Integration | auth_core | ✅ Verified | 5 tests passed |
| Integration | inventory_sales | ✅ Verified | 2 tests passed |
| Integration | sales_accounting | ✅ Verified | 4 tests passed |
| Integration | purchase_inventory | ✅ Verified | 4 tests passed |
| Integration | inventory_reporting | ✅ Verified | 4 tests passed |
| E2E | sales_flow | ✅ Verified | 2 tests passed |
| E2E | inventory_flow | ⚠️ Partial | 2 tests passed, 2 tests failed (missing supplier_data fixture) |
| E2E | purchase_flow | ⚠️ Partial | 1 test passed, 2 tests failed (missing supplier_data fixture) |
| E2E | accounting_flow | ❌ Failed | All tests failed (missing EVENT_TYPES constants) |
| E2E | reporting_flow | ⚠️ Partial | 3 tests passed, 1 test failed (missing EVENT_TYPES constant) |
| Performance | api_load | ✅ Verified | 1 test passed |
| Performance | database_load | ❌ Failed | Import error (No module named 'common.models') |
| Performance | kafka_throughput | ❌ Failed | Import error (cannot import name 'BOOTSTRAP_SERVERS') |
| Security | auth_security | ✅ Verified | 10 tests passed |
| Security | api_security | ❌ Failed | Import error (cannot import name 'generate_jwt_token') |
| Security | data_security | ❌ Failed | Import error (No module named 'common.models') |

## Continuous Integration

The testing framework is designed to be integrated with CI/CD pipelines. The JUnit XML reports can be used by CI systems to display test results, and the coverage reports can be used to track code coverage over time.

## Common Issues

1. **Missing Fixtures**: Several E2E tests failed due to missing the `supplier_data` fixture. This needs to be added to the test fixtures.

2. **Missing Constants**: Several tests failed due to missing constants in the `EVENT_TYPES` dictionary. The following constants need to be added:
   - `SALES_TRANSACTION_CREATED`
   - `PURCHASE_PAYMENT_CREATED`
   - `TAX_REPORT_GENERATED`
   - `DASHBOARD_DATA_UPDATED`

3. **Import Errors**: Several tests failed due to import errors:
   - `common.models` module not found
   - `BOOTSTRAP_SERVERS` not found in `common.kafka_config`
   - `generate_jwt_token` not found in `common.jwt_auth`

## Next Steps

1. Fix missing fixtures (supplier_data) in E2E tests
2. Add missing EVENT_TYPES constants for various event flows
3. Fix import errors in performance and security tests
4. Fix Django configuration for unit tests
5. Add code coverage reporting
6. Set up CI/CD pipeline for automated testing

## Best Practices

1. **Write tests first**: Follow a test-driven development (TDD) approach when implementing new features.
2. **Keep tests independent**: Each test should be independent of other tests and should not rely on the state created by other tests.
3. **Use meaningful test names**: Test names should clearly describe what is being tested.
4. **Use fixtures**: Use fixtures to set up test data and avoid duplicating code.
5. **Mock external dependencies**: Use mock objects to simulate external dependencies and avoid making actual API calls or database queries.
6. **Test edge cases**: Test both the happy path and edge cases, including error conditions.
7. **Keep tests fast**: Tests should run quickly to provide fast feedback.
8. **Maintain test coverage**: Aim for high test coverage, especially for critical business logic.

## Troubleshooting

### Common Issues

1. **Tests failing due to Django configuration**: Ensure that the models are properly configured with explicit app_labels or included in INSTALLED_APPS.
2. **Kafka connection issues**: Ensure that Kafka is running and accessible from the test environment.
3. **Database connection issues**: Ensure that the database is running and accessible from the test environment.
4. **Test data conflicts**: Ensure that tests clean up after themselves to avoid conflicts with other tests.

### Debugging Tips

1. **Use verbose output**: Run tests with the `--verbose` option to see more detailed output.
2. **Inspect test logs**: Check the test logs for error messages and stack traces.
3. **Use pdb**: Insert `import pdb; pdb.set_trace()` in the test code to debug interactively.
4. **Check test fixtures**: Ensure that test fixtures are correctly set up and provide the expected data.
