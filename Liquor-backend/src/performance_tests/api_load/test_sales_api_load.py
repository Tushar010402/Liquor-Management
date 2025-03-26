"""
Performance test for the sales API in the Liquor Management System.
This test verifies that the sales API can handle the expected load.
"""

import os
import json
import time
import uuid
import random
from datetime import datetime
from locust import HttpUser, task, between

# Configuration
NUM_USERS = int(os.getenv('NUM_USERS', '100'))
SPAWN_RATE = int(os.getenv('SPAWN_RATE', '10'))
RUN_TIME = os.getenv('RUN_TIME', '5m')
HOST = os.getenv('HOST', 'http://localhost:8004')  # Sales service port

# Test data
SHOP_IDS = [str(uuid.uuid4()) for _ in range(5)]
BRAND_IDS = [str(uuid.uuid4()) for _ in range(20)]
USER_IDS = [str(uuid.uuid4()) for _ in range(10)]
TENANT_ID = str(uuid.uuid4())

# Authentication token (would be generated dynamically in a real test)
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNDU2Nzg5MCIsInRlbmFudF9pZCI6IjA5ODc2NTQzMjEiLCJyb2xlIjoibWFuYWdlciIsImV4cCI6MTcxNjQwNjQwMH0.signature"

class SalesUser(HttpUser):
    """
    Simulated user for sales API load testing.
    """
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks
    
    def on_start(self):
        """
        Set up the user before starting tasks.
        """
        self.client.headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Content-Type': 'application/json'
        }
    
    @task(10)  # Higher weight for this common task
    def create_sale(self):
        """
        Create a new sale.
        """
        # Generate random sale data
        shop_id = random.choice(SHOP_IDS)
        num_items = random.randint(1, 5)
        items = []
        
        for _ in range(num_items):
            brand_id = random.choice(BRAND_IDS)
            quantity = random.randint(1, 3)
            unit_price = random.uniform(100, 1000)
            total_price = quantity * unit_price
            tax_amount = total_price * 0.18  # Assuming 18% tax
            
            items.append({
                'brand_id': brand_id,
                'quantity': quantity,
                'price_type': random.choice(['regular', 'discount']),
                'unit_price': unit_price,
                'total_price': total_price,
                'tax_amount': tax_amount
            })
        
        # Calculate totals
        subtotal = sum(item['total_price'] for item in items)
        tax_total = sum(item['tax_amount'] for item in items)
        grand_total = subtotal + tax_total
        
        # Create sale payload
        payload = {
            'shop_id': shop_id,
            'items': items,
            'payment_method': random.choice(['cash', 'upi', 'card']),
            'tenant_id': TENANT_ID
        }
        
        # Send request
        start_time = time.time()
        response = self.client.post('/api/sales', json=payload)
        request_time = time.time() - start_time
        
        # Log performance metrics
        if response.status_code == 201:
            self.environment.events.request_success.fire(
                request_type='POST',
                name='Create Sale',
                response_time=request_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )
        else:
            self.environment.events.request_failure.fire(
                request_type='POST',
                name='Create Sale',
                response_time=request_time * 1000,  # Convert to milliseconds
                exception=Exception(f"Failed with status code: {response.status_code}")
            )
    
    @task(5)
    def get_sales_list(self):
        """
        Get a list of sales.
        """
        # Randomly select query parameters
        shop_id = random.choice(SHOP_IDS)
        page = random.randint(1, 5)
        limit = random.choice([10, 20, 50])
        
        # Send request
        start_time = time.time()
        response = self.client.get(f'/api/sales?shop_id={shop_id}&page={page}&limit={limit}')
        request_time = time.time() - start_time
        
        # Log performance metrics
        if response.status_code == 200:
            self.environment.events.request_success.fire(
                request_type='GET',
                name='List Sales',
                response_time=request_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )
        else:
            self.environment.events.request_failure.fire(
                request_type='GET',
                name='List Sales',
                response_time=request_time * 1000,  # Convert to milliseconds
                exception=Exception(f"Failed with status code: {response.status_code}")
            )
    
    @task(3)
    def get_sale_details(self):
        """
        Get details of a specific sale.
        """
        # In a real test, we would get an actual sale ID from a previous request
        # For this example, we'll use a random UUID
        sale_id = str(uuid.uuid4())
        
        # Send request
        start_time = time.time()
        response = self.client.get(f'/api/sales/{sale_id}')
        request_time = time.time() - start_time
        
        # Log performance metrics
        if response.status_code in [200, 404]:  # 404 is expected for random IDs
            self.environment.events.request_success.fire(
                request_type='GET',
                name='Get Sale Details',
                response_time=request_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )
        else:
            self.environment.events.request_failure.fire(
                request_type='GET',
                name='Get Sale Details',
                response_time=request_time * 1000,  # Convert to milliseconds
                exception=Exception(f"Failed with status code: {response.status_code}")
            )
    
    @task(2)
    def approve_sale(self):
        """
        Approve a sale.
        """
        # In a real test, we would get an actual sale ID from a previous request
        # For this example, we'll use a random UUID
        sale_id = str(uuid.uuid4())
        
        # Create approval payload
        payload = {
            'comments': 'Approved in performance test'
        }
        
        # Send request
        start_time = time.time()
        response = self.client.post(f'/api/sales/{sale_id}/approve', json=payload)
        request_time = time.time() - start_time
        
        # Log performance metrics
        if response.status_code in [200, 404]:  # 404 is expected for random IDs
            self.environment.events.request_success.fire(
                request_type='POST',
                name='Approve Sale',
                response_time=request_time * 1000,  # Convert to milliseconds
                response_length=len(response.content)
            )
        else:
            self.environment.events.request_failure.fire(
                request_type='POST',
                name='Approve Sale',
                response_time=request_time * 1000,  # Convert to milliseconds
                exception=Exception(f"Failed with status code: {response.status_code}")
            )

# Performance test execution script
if __name__ == '__main__':
    import subprocess
    import sys
    
    print(f"Starting performance test with {NUM_USERS} users, spawn rate {SPAWN_RATE}, run time {RUN_TIME}")
    
    # Build the locust command
    cmd = [
        "locust",
        "-f", __file__,
        "--headless",
        "-u", str(NUM_USERS),
        "-r", str(SPAWN_RATE),
        "--run-time", RUN_TIME,
        "--host", HOST
    ]
    
    # Run the locust command
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    
    # Exit with the same code as the locust command
    sys.exit(result.returncode)
