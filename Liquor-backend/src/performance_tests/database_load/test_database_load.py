"""
Performance tests for database load in the Liquor Management System.
These tests measure the database performance under load, including read operations,
write operations, query performance, and transaction throughput.
"""

import time
import uuid
import pytest
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor
from django.db import connection, transaction
from django.utils import timezone
from datetime import datetime, timedelta

# Import models from different services
from inventory_service.products.models import Brand, Product
from inventory_service.stock.models import StockLevel
from sales_service.sales.models import Sale, SaleItem
from purchase_service.purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from accounting_service.accounts.models import Account
from accounting_service.journals.models import JournalEntry, RecurringJournalEntry

# Test configuration
NUM_THREADS = 10
NUM_OPERATIONS = 100
BATCH_SIZE = 20

class TestDatabaseReadPerformance:
    """
    Test the read performance of the database under load.
    """
    
    @pytest.fixture(scope="class")
    def setup_test_data(self, db):
        """Set up test data for read performance tests."""
        # Create test brands
        brands = []
        for i in range(100):
            brand = Brand.objects.create(
                name=f"Test Brand {i}",
                category="whisky",
                regular_price=500.0 + (i * 10),
                discounted_price=450.0 + (i * 10),
                tax_rate=18.0,
                status="active",
                tenant_id=str(uuid.uuid4()),
                shop_id=str(uuid.uuid4())
            )
            brands.append(brand)
        
        # Create test products and stock
        stocks = []
        for brand in brands:
            # Create a product for each brand
            product = Product.objects.create(
                name=f"Test Product for {brand.name}",
                code=f"TP-{brand.code}",
                brand=brand,
                mrp=550.0,
                selling_price=500.0,
                purchase_price=400.0,
                tax_rate=18.0,
                tenant_id=brand.tenant_id,
                shop_id=brand.shop_id
            )
            
            # Create stock for the product
            stock = StockLevel.objects.create(
                product=product,
                current_stock=100,
                minimum_stock=10,
                maximum_stock=100,
                tenant_id=brand.tenant_id,
                shop_id=brand.shop_id
            )
            stocks.append(stock)
        
        # Create test sales
        sales = []
        for i in range(50):
            sale = Sale.objects.create(
                invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{i:06d}",
                total_amount=1000.0 + (i * 100),
                tax_amount=180.0 + (i * 18),
                discount_amount=0.0,
                grand_total=1180.0 + (i * 118),
                payment_method="cash",
                status="completed",
                tenant_id=brands[0].tenant_id,
                shop_id=brands[0].shop_id,
                created_by=str(uuid.uuid4())
            )
            sales.append(sale)
            
            # Create sale items
            for j in range(5):
                brand_index = (i + j) % len(brands)
                SaleItem.objects.create(
                    sale=sale,
                    brand=brands[brand_index],
                    quantity=j + 1,
                    unit_price=brands[brand_index].regular_price,
                    total_price=(j + 1) * brands[brand_index].regular_price,
                    tax_amount=(j + 1) * brands[brand_index].regular_price * 0.18
                )
        
        return {
            'brands': brands,
            'stocks': stocks,
            'sales': sales,
            'tenant_id': brands[0].tenant_id,
            'shop_id': brands[0].shop_id
        }
    
    def test_simple_query_performance(self, db, setup_test_data):
        """Test the performance of simple queries."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_query():
            start_time = time.time()
            brands = Brand.objects.filter(tenant_id=tenant_id, shop_id=shop_id)
            query_time = time.time() - start_time
            return query_time
        
        # Execute queries in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            query_times = list(executor.map(lambda _: execute_query(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(query_times)
        max_time = max(query_times)
        min_time = min(query_times)
        p95_time = sorted(query_times)[int(NUM_OPERATIONS * 0.95)]
        
        print(f"\nSimple Query Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Queries per second: {NUM_OPERATIONS / sum(query_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.05, f"Average query time ({avg_time:.6f}s) exceeds threshold (0.05s)"
        assert p95_time < 0.1, f"95th percentile query time ({p95_time:.6f}s) exceeds threshold (0.1s)"
    
    def test_complex_query_performance(self, db, setup_test_data):
        """Test the performance of complex queries with joins."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_complex_query():
            start_time = time.time()
            # Query with joins and aggregations
            sales_data = Sale.objects.filter(
                tenant_id=tenant_id,
                shop_id=shop_id,
                status="completed"
            ).select_related(
                'created_by'
            ).prefetch_related(
                'saleitems__brand'
            )
            
            # Force evaluation
            results = list(sales_data)
            query_time = time.time() - start_time
            return query_time
        
        # Execute queries in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            query_times = list(executor.map(lambda _: execute_complex_query(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(query_times)
        max_time = max(query_times)
        min_time = min(query_times)
        p95_time = sorted(query_times)[int(NUM_OPERATIONS * 0.95)]
        
        print(f"\nComplex Query Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Queries per second: {NUM_OPERATIONS / sum(query_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.1, f"Average complex query time ({avg_time:.6f}s) exceeds threshold (0.1s)"
        assert p95_time < 0.2, f"95th percentile complex query time ({p95_time:.6f}s) exceeds threshold (0.2s)"
    
    def test_aggregation_query_performance(self, db, setup_test_data):
        """Test the performance of aggregation queries."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_aggregation_query():
            start_time = time.time()
            # Query with aggregations
            from django.db.models import Sum, Count, Avg
            
            sales_summary = Sale.objects.filter(
                tenant_id=tenant_id,
                shop_id=shop_id,
                status="completed"
            ).values(
                'payment_method'
            ).annotate(
                total_sales=Sum('grand_total'),
                count=Count('id'),
                avg_sale=Avg('grand_total')
            )
            
            # Force evaluation
            results = list(sales_summary)
            query_time = time.time() - start_time
            return query_time
        
        # Execute queries in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            query_times = list(executor.map(lambda _: execute_aggregation_query(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(query_times)
        max_time = max(query_times)
        min_time = min(query_times)
        p95_time = sorted(query_times)[int(NUM_OPERATIONS * 0.95)]
        
        print(f"\nAggregation Query Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Queries per second: {NUM_OPERATIONS / sum(query_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.1, f"Average aggregation query time ({avg_time:.6f}s) exceeds threshold (0.1s)"
        assert p95_time < 0.2, f"95th percentile aggregation query time ({p95_time:.6f}s) exceeds threshold (0.2s)"

class TestDatabaseWritePerformance:
    """
    Test the write performance of the database under load.
    """
    
    @pytest.fixture(scope="class")
    def setup_test_data(self, db):
        """Set up test data for write performance tests."""
        tenant_id = str(uuid.uuid4())
        shop_id = str(uuid.uuid4())
        
        # Create test brands
        brands = []
        for i in range(20):
            brand = Brand.objects.create(
                name=f"Test Brand {i}",
                category="whisky",
                regular_price=500.0 + (i * 10),
                discounted_price=450.0 + (i * 10),
                tax_rate=18.0,
                status="active",
                tenant_id=tenant_id,
                shop_id=shop_id
            )
            brands.append(brand)
        
        return {
            'brands': brands,
            'tenant_id': tenant_id,
            'shop_id': shop_id
        }
    
    def test_single_insert_performance(self, db, setup_test_data):
        """Test the performance of single insert operations."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_insert():
            start_time = time.time()
            brand = Brand.objects.create(
                name=f"Performance Test Brand {uuid.uuid4()}",
                category="whisky",
                regular_price=500.0,
                discounted_price=450.0,
                tax_rate=18.0,
                status="active",
                tenant_id=tenant_id,
                shop_id=shop_id
            )
            insert_time = time.time() - start_time
            return insert_time
        
        # Execute inserts in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            insert_times = list(executor.map(lambda _: execute_insert(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(insert_times)
        max_time = max(insert_times)
        min_time = min(insert_times)
        p95_time = sorted(insert_times)[int(NUM_OPERATIONS * 0.95)]
        
        print(f"\nSingle Insert Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Inserts per second: {NUM_OPERATIONS / sum(insert_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.05, f"Average insert time ({avg_time:.6f}s) exceeds threshold (0.05s)"
        assert p95_time < 0.1, f"95th percentile insert time ({p95_time:.6f}s) exceeds threshold (0.1s)"
    
    def test_batch_insert_performance(self, db, setup_test_data):
        """Test the performance of batch insert operations."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_batch_insert():
            start_time = time.time()
            
            with transaction.atomic():
                brands_to_create = [
                    Brand(
                        name=f"Batch Test Brand {uuid.uuid4()}",
                        category="whisky",
                        regular_price=500.0,
                        discounted_price=450.0,
                        tax_rate=18.0,
                        status="active",
                        tenant_id=tenant_id,
                        shop_id=shop_id
                    )
                    for _ in range(BATCH_SIZE)
                ]
                
                Brand.objects.bulk_create(brands_to_create)
            
            insert_time = time.time() - start_time
            return insert_time
        
        # Execute batch inserts in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            batch_times = list(executor.map(lambda _: execute_batch_insert(), range(NUM_OPERATIONS // BATCH_SIZE)))
        
        # Calculate statistics
        avg_time = statistics.mean(batch_times)
        max_time = max(batch_times)
        min_time = min(batch_times)
        p95_time = sorted(batch_times)[int(len(batch_times) * 0.95)]
        total_records = NUM_OPERATIONS
        
        print(f"\nBatch Insert Performance ({BATCH_SIZE} records per batch):")
        print(f"Average time per batch: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Records per second: {total_records / sum(batch_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.2, f"Average batch insert time ({avg_time:.6f}s) exceeds threshold (0.2s)"
        assert p95_time < 0.4, f"95th percentile batch insert time ({p95_time:.6f}s) exceeds threshold (0.4s)"
    
    def test_transaction_performance(self, db, setup_test_data):
        """Test the performance of complex transactions."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        brands = setup_test_data['brands']
        
        # Function to execute in threads
        def execute_transaction():
            start_time = time.time()
            
            with transaction.atomic():
                # Create a sale
                sale = Sale.objects.create(
                    invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
                    total_amount=1000.0,
                    tax_amount=180.0,
                    discount_amount=0.0,
                    grand_total=1180.0,
                    payment_method="cash",
                    status="completed",
                    tenant_id=tenant_id,
                    shop_id=shop_id,
                    created_by=str(uuid.uuid4())
                )
                
                # Create sale items
                sale_items = []
                for i in range(5):
                    brand_index = i % len(brands)
                    sale_items.append(
                        SaleItem(
                            sale=sale,
                            brand=brands[brand_index],
                            quantity=i + 1,
                            unit_price=brands[brand_index].regular_price,
                            total_price=(i + 1) * brands[brand_index].regular_price,
                            tax_amount=(i + 1) * brands[brand_index].regular_price * 0.18
                        )
                    )
                
                SaleItem.objects.bulk_create(sale_items)
                
                # Update stock
                for i, item in enumerate(sale_items):
                    stock = StockLevel.objects.get(product=item.brand.product)
                    stock.current_stock -= item.quantity
                    stock.save()
            
            transaction_time = time.time() - start_time
            return transaction_time
        
        # Execute transactions in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            transaction_times = list(executor.map(lambda _: execute_transaction(), range(NUM_OPERATIONS // 5)))
        
        # Calculate statistics
        avg_time = statistics.mean(transaction_times)
        max_time = max(transaction_times)
        min_time = min(transaction_times)
        p95_time = sorted(transaction_times)[int(len(transaction_times) * 0.95)]
        
        print(f"\nComplex Transaction Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Transactions per second: {(NUM_OPERATIONS // 5) / sum(transaction_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.3, f"Average transaction time ({avg_time:.6f}s) exceeds threshold (0.3s)"
        assert p95_time < 0.5, f"95th percentile transaction time ({p95_time:.6f}s) exceeds threshold (0.5s)"

class TestDatabaseScalabilityPerformance:
    """
    Test the scalability of the database under increasing load.
    """
    
    @pytest.fixture(scope="class")
    def setup_test_data(self, db):
        """Set up test data for scalability tests."""
        tenant_id = str(uuid.uuid4())
        shop_id = str(uuid.uuid4())
        
        # Create test brands
        brands = []
        for i in range(20):
            brand = Brand.objects.create(
                name=f"Test Brand {i}",
                category="whisky",
                regular_price=500.0 + (i * 10),
                discounted_price=450.0 + (i * 10),
                tax_rate=18.0,
                status="active",
                tenant_id=tenant_id,
                shop_id=shop_id
            )
            brands.append(brand)
        
        return {
            'brands': brands,
            'tenant_id': tenant_id,
            'shop_id': shop_id
        }
    
    @pytest.mark.parametrize("num_threads", [1, 5, 10, 20])
    def test_read_scalability(self, db, setup_test_data, num_threads):
        """Test the scalability of read operations with increasing thread count."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_query():
            start_time = time.time()
            brands = Brand.objects.filter(tenant_id=tenant_id, shop_id=shop_id)
            # Force evaluation
            results = list(brands)
            query_time = time.time() - start_time
            return query_time
        
        # Execute queries in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            query_times = list(executor.map(lambda _: execute_query(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(query_times)
        max_time = max(query_times)
        min_time = min(query_times)
        p95_time = sorted(query_times)[int(NUM_OPERATIONS * 0.95)]
        throughput = NUM_OPERATIONS / sum(query_times)
        
        print(f"\nRead Scalability ({num_threads} threads):")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Queries per second: {throughput:.2f}")
        
        return throughput
    
    @pytest.mark.parametrize("num_threads", [1, 5, 10, 20])
    def test_write_scalability(self, db, setup_test_data, num_threads):
        """Test the scalability of write operations with increasing thread count."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_insert():
            start_time = time.time()
            brand = Brand.objects.create(
                name=f"Scalability Test Brand {uuid.uuid4()}",
                category="whisky",
                regular_price=500.0,
                discounted_price=450.0,
                tax_rate=18.0,
                status="active",
                tenant_id=tenant_id,
                shop_id=shop_id
            )
            insert_time = time.time() - start_time
            return insert_time
        
        # Execute inserts in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            insert_times = list(executor.map(lambda _: execute_insert(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(insert_times)
        max_time = max(insert_times)
        min_time = min(insert_times)
        p95_time = sorted(insert_times)[int(NUM_OPERATIONS * 0.95)]
        throughput = NUM_OPERATIONS / sum(insert_times)
        
        print(f"\nWrite Scalability ({num_threads} threads):")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Inserts per second: {throughput:.2f}")
        
        return throughput
    
    def test_connection_pool_performance(self, db, setup_test_data):
        """Test the performance of the database connection pool."""
        tenant_id = setup_test_data['tenant_id']
        shop_id = setup_test_data['shop_id']
        
        # Function to execute in threads
        def execute_query_with_connection():
            start_time = time.time()
            
            # Get a connection from the pool
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM products_brand WHERE tenant_id = %s AND shop_id = %s",
                    [tenant_id, shop_id]
                )
                results = cursor.fetchall()
            
            query_time = time.time() - start_time
            return query_time
        
        # Execute queries in parallel
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            query_times = list(executor.map(lambda _: execute_query_with_connection(), range(NUM_OPERATIONS)))
        
        # Calculate statistics
        avg_time = statistics.mean(query_times)
        max_time = max(query_times)
        min_time = min(query_times)
        p95_time = sorted(query_times)[int(NUM_OPERATIONS * 0.95)]
        
        print(f"\nConnection Pool Performance:")
        print(f"Average time: {avg_time:.6f} seconds")
        print(f"Max time: {max_time:.6f} seconds")
        print(f"Min time: {min_time:.6f} seconds")
        print(f"95th percentile: {p95_time:.6f} seconds")
        print(f"Queries per second: {NUM_OPERATIONS / sum(query_times):.2f}")
        
        # Assert performance criteria
        assert avg_time < 0.05, f"Average connection pool query time ({avg_time:.6f}s) exceeds threshold (0.05s)"
        assert p95_time < 0.1, f"95th percentile connection pool query time ({p95_time:.6f}s) exceeds threshold (0.1s)"
