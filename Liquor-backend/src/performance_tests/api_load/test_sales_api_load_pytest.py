"""
Pytest wrapper for the sales API load test.
"""

import pytest
from unittest.mock import patch, MagicMock

# Import the locust test
from .test_sales_api_load import SalesUser

# Create a subclass of SalesUser with the host attribute set
class TestSalesUser(SalesUser):
    host = "http://localhost:8004"

def test_sales_api_load():
    """
    Test that the sales API load test can be initialized.
    This is a simple wrapper to make pytest happy.
    In a real scenario, you would run the locust test directly.
    """
    # Create a mock environment
    mock_env = MagicMock()
    mock_env.events.request_success = MagicMock()
    mock_env.events.request_failure = MagicMock()
    
    # Create a mock client
    mock_client = MagicMock()
    mock_client.post.return_value = MagicMock(status_code=201, content=b'{"id": "123"}')
    mock_client.get.return_value = MagicMock(status_code=200, content=b'{"id": "123"}')
    
    # Create a TestSalesUser instance
    user = TestSalesUser(mock_env)
    user.client = mock_client
    
    # Call on_start to set up the user
    user.on_start()
    
    # Verify that the headers were set correctly
    assert 'Authorization' in user.client.headers
    assert 'Content-Type' in user.client.headers
    
    # This test doesn't actually run the load test, it just verifies that the
    # SalesUser class can be instantiated and initialized correctly.
    # To run the actual load test, use the locust command directly.
    
    # For example:
    # locust -f src/performance_tests/api_load/test_sales_api_load.py --headless -u 10 -r 1 --run-time 10s
