# Liquor Management System Test Fix Plan

This document outlines the plan to fix the issues found in the tests for the Liquor Management System backend.

## Issues Summary

Based on the test results, we have identified the following issues:

1. **Missing Fixtures**: Several E2E tests failed due to missing the `supplier_data` fixture.
2. **Missing Constants**: Several tests failed due to missing constants in the `EVENT_TYPES` dictionary.
3. **Import Errors**: Several tests failed due to import errors related to missing modules or functions.
4. **Django Configuration Issues**: Unit tests are failing due to Django configuration issues.

## Detailed Fix Plan

### 1. Fix Missing Fixtures

#### Issue: Missing `supplier_data` fixture in E2E tests

The following tests are failing due to missing the `supplier_data` fixture:
- `inventory_flow/test_inventory_e2e.py::TestInventoryE2EFlow::test_stock_receipt_flow`
- `inventory_flow/test_inventory_e2e.py::TestInventoryE2EFlow::test_low_stock_alert_flow`
- `purchase_flow/test_purchase_e2e.py::TestPurchaseE2EFlow::test_purchase_order_to_goods_receipt_flow`
- `purchase_flow/test_purchase_e2e.py::TestPurchaseE2EFlow::test_purchase_order_rejection_flow`

#### Solution:

Add the `supplier_data` fixture to the `src/e2e_tests/conftest.py` file:

```python
@pytest.fixture
def supplier_data():
    """
    Fixture to provide supplier data for tests.
    """
    return {
        'id': str(uuid.uuid4()),
        'name': 'Test Supplier',
        'contact_name': 'John Supplier',
        'email': 'supplier@example.com',
        'phone': '9876543210',
        'address': '789 Supplier St, Supplier City',
        'tax_id': 'SUPP123456',
        'payment_terms': 'Net 30',
        'tenant_id': str(uuid.uuid4()),
        'shop_id': str(uuid.uuid4()),
        'status': 'active',
        'created_at': timezone.now().isoformat(),
        'updated_at': timezone.now().isoformat()
    }
```

### 2. Fix Missing Constants

#### Issue: Missing constants in the `EVENT_TYPES` dictionary

The following tests are failing due to missing constants:
- `accounting_flow/test_accounting_e2e.py::TestAccountingE2EFlow::test_sales_transaction_accounting_flow` - Missing `SALES_TRANSACTION_CREATED`
- `accounting_flow/test_accounting_e2e.py::TestAccountingE2EFlow::test_purchase_transaction_accounting_flow` - Missing `PURCHASE_PAYMENT_CREATED`
- `accounting_flow/test_accounting_e2e.py::TestAccountingE2EFlow::test_tax_calculation_and_reporting` - Missing `TAX_REPORT_GENERATED`
- `reporting_flow/test_reporting_e2e.py::TestReportingE2EFlow::test_dashboard_data_generation_flow` - Missing `DASHBOARD_DATA_UPDATED`

#### Solution:

Add the missing constants to the `src/common/kafka_config.py` file:

```python
EVENT_TYPES = {
    # Existing constants
    ...
    
    # Add missing constants
    'SALES_TRANSACTION_CREATED': 'sales_transaction_created',
    'PURCHASE_PAYMENT_CREATED': 'purchase_payment_created',
    'TAX_REPORT_GENERATED': 'tax_report_generated',
    'DASHBOARD_DATA_UPDATED': 'dashboard_data_updated'
}
```

### 3. Fix Import Errors

#### Issue 3.1: Missing `common.models` module

The following tests are failing due to missing the `common.models` module:
- `database_load/test_database_load.py` - Import error (No module named 'common.models')
- `data_security/test_data_security.py` - Import error (No module named 'common.models')

#### Solution 3.1:

Create or update the `src/common/models.py` file to include the required models:

```python
from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    """
    Base model for all models in the system.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'common'

class TenantAwareModel(BaseModel):
    """
    Base model for all tenant-aware models in the system.
    """
    tenant_id = models.UUIDField()
    shop_id = models.UUIDField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'common'
```

#### Issue 3.2: Missing `BOOTSTRAP_SERVERS` in `common.kafka_config`

The following test is failing due to missing `BOOTSTRAP_SERVERS` in `common.kafka_config`:
- `kafka_throughput/test_kafka_throughput.py` - Import error (cannot import name 'BOOTSTRAP_SERVERS')

#### Solution 3.2:

Add the `BOOTSTRAP_SERVERS` constant to the `src/common/kafka_config.py` file:

```python
# Kafka configuration
BOOTSTRAP_SERVERS = ['kafka:9092']
```

#### Issue 3.3: Missing `generate_jwt_token` in `common.jwt_auth`

The following test is failing due to missing `generate_jwt_token` in `common.jwt_auth`:
- `api_security/test_api_security.py` - Import error (cannot import name 'generate_jwt_token')

#### Solution 3.3:

Add the `generate_jwt_token` function to the `src/common/jwt_auth.py` file:

```python
import jwt
from datetime import datetime, timedelta
import uuid

# JWT configuration
JWT_SECRET_KEY = 'your-secret-key'  # In production, this should be stored securely
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 3600  # 1 hour

def generate_jwt_token(user_id, tenant_id, shop_id=None, role='user'):
    """
    Generate a JWT token for the given user.
    """
    payload = {
        'user_id': str(user_id),
        'tenant_id': str(tenant_id),
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4())
    }
    
    if shop_id:
        payload['shop_id'] = str(shop_id)
    
    payload['role'] = role
    
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token):
    """
    Decode a JWT token and return the payload.
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')
```

### 4. Fix Django Configuration Issues

#### Issue: Unit tests failing due to Django configuration issues

Unit tests are failing because the models are not properly configured with explicit app_labels or included in INSTALLED_APPS.

#### Solution:

1. Update the `test_settings.py` file to include all the required apps:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add all service apps
    'auth_service',
    'auth_service.authentication',
    'auth_service.roles',
    'auth_service.tenants',
    'auth_service.users',
    'auth_service.shops',
    
    'core_service',
    'core_service.tenants',
    'core_service.shops',
    'core_service.settings',
    
    'inventory_service',
    'inventory_service.brands',
    'inventory_service.products',
    'inventory_service.stock',
    'inventory_service.suppliers',
    
    'purchase_service',
    'purchase_service.purchase_orders',
    'purchase_service.goods_receipt',
    'purchase_service.suppliers',
    
    'sales_service',
    'sales_service.sales',
    'sales_service.approvals',
    'sales_service.returns',
    'sales_service.cash',
    
    'accounting_service',
    'accounting_service.accounts',
    'accounting_service.journals',
    'accounting_service.ledger',
    'accounting_service.reconciliation',
    'accounting_service.reports',
    'accounting_service.taxes',
    
    'reporting_service',
    'reporting_service.analytics',
    'reporting_service.dashboards',
    'reporting_service.financial_reports',
    'reporting_service.inventory_reports',
    'reporting_service.performance_reports',
    'reporting_service.sales_reports',
    'reporting_service.tax_reports',
    
    # Common app
    'common',
]
```

2. Ensure all models have explicit app_labels in their Meta classes:

```python
class Meta:
    app_label = 'app_name'
```

## Implementation Plan

1. **Fix Missing Fixtures**: Add the `supplier_data` fixture to the `src/e2e_tests/conftest.py` file.
2. **Fix Missing Constants**: Add the missing constants to the `src/common/kafka_config.py` file.
3. **Fix Import Errors**: Create or update the required modules and functions.
4. **Fix Django Configuration Issues**: Update the `test_settings.py` file and ensure all models have explicit app_labels.
5. **Run Tests**: Run the tests again to verify that the fixes have resolved the issues.
6. **Update Documentation**: Update the test documentation to reflect the current status of the tests.

## Conclusion

By implementing the fixes outlined in this plan, we should be able to resolve the issues found in the tests and improve the overall test coverage and reliability of the Liquor Management System backend.
