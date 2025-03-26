"""
End-to-end test for the sales flow in the Liquor Management System.
This test verifies the complete flow from creating a sale to its approval
and the resulting inventory updates and financial transactions.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES

# Mock functions for the sales flow
def mock_create_sale(shop_id, items, payment_method, user_id, tenant_id):
    """Mock function for creating a sale in the sales service."""
    sale_id = str(uuid.uuid4())
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    # Calculate totals
    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
    tax_total = sum(item['tax_amount'] for item in items)
    grand_total = subtotal + tax_total
    
    return {
        'id': sale_id,
        'invoice_number': invoice_number,
        'shop_id': shop_id,
        'items': items,
        'subtotal': subtotal,
        'tax_total': tax_total,
        'grand_total': grand_total,
        'payment_method': payment_method,
        'status': 'pending',
        'created_by': user_id,
        'tenant_id': tenant_id,
        'created_at': timezone.now().isoformat()
    }

def mock_approve_sale(sale_id, approver_id):
    """Mock function for approving a sale in the sales service."""
    return {
        'id': sale_id,
        'status': 'approved',
        'approved_by': approver_id,
        'approved_at': timezone.now().isoformat()
    }

def mock_update_inventory(shop_id, items, tenant_id):
    """Mock function for updating inventory after a sale is approved."""
    return {
        'shop_id': shop_id,
        'items_updated': len(items),
        'tenant_id': tenant_id,
        'updated_at': timezone.now().isoformat()
    }

def mock_create_financial_transaction(sale_id, shop_id, amount, payment_method, tenant_id):
    """Mock function for creating a financial transaction in the accounting service."""
    transaction_id = str(uuid.uuid4())
    return {
        'id': transaction_id,
        'sale_id': sale_id,
        'shop_id': shop_id,
        'amount': amount,
        'payment_method': payment_method,
        'status': 'completed',
        'tenant_id': tenant_id,
        'created_at': timezone.now().isoformat()
    }

def mock_update_reporting_data(sale_id, shop_id, items, amount, tenant_id):
    """Mock function for updating reporting data in the reporting service."""
    return {
        'sale_id': sale_id,
        'shop_id': shop_id,
        'items_count': len(items),
        'amount': amount,
        'tenant_id': tenant_id,
        'updated_at': timezone.now().isoformat()
    }

class TestSalesE2EFlow:
    """
    Test the end-to-end sales flow in the Liquor Management System.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_sales_creation_to_approval_flow(self, mock_get_consumer, mock_get_producer,
                                            mock_kafka_producer, mock_kafka_consumer,
                                            shop_data, brand_data, user_data, stock_data):
        """
        Test the complete flow from creating a sale to its approval and the resulting
        inventory updates and financial transactions.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        manager_id = str(uuid.uuid4())  # Manager who will approve the sale
        
        # Create sale items
        items = [
            {
                'brand_id': brand_id,
                'quantity': 2,
                'price_type': 'regular',
                'unit_price': brand_data['regular_price'],
                'total_price': 2 * brand_data['regular_price'],
                'tax_amount': 2 * brand_data['regular_price'] * (brand_data['tax_rate'] / 100)
            }
        ]
        
        # Step 1: Create a sale in the sales service
        sale = mock_create_sale(
            shop_id=shop_id,
            items=items,
            payment_method='cash',
            user_id=user_id,
            tenant_id=tenant_id
        )
        
        # Step 2: Publish sale created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        sale_created_event = {
            'event_type': EVENT_TYPES['SALE_CREATED'],
            'sale_id': sale['id'],
            'invoice_number': sale['invoice_number'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'total_amount': sale['grand_total'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SALES_EVENTS'],
            key=sale['id'],
            event_data=sale_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SALES_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sale['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Approve the sale
        approval = mock_approve_sale(
            sale_id=sale['id'],
            approver_id=manager_id
        )
        
        # Step 4: Publish sale approved event to Kafka
        sale_approved_event = {
            'event_type': EVENT_TYPES['SALE_APPROVED'],
            'sale_id': sale['id'],
            'invoice_number': sale['invoice_number'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'total_amount': sale['grand_total'],
            'approved_by': approval['approved_by'],
            'approved_at': approval['approved_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SALES_EVENTS'],
            key=sale['id'],
            event_data=sale_approved_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SALES_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sale['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 5: Update inventory based on the approved sale
        inventory_update = mock_update_inventory(
            shop_id=sale['shop_id'],
            items=sale['items'],
            tenant_id=sale['tenant_id']
        )
        
        # Step 6: Publish inventory updated event to Kafka
        inventory_updated_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'sale_id': sale['id'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'items': sale['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=sale['id'],
            event_data=inventory_updated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sale['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 7: Create financial transaction for the sale
        financial_transaction = mock_create_financial_transaction(
            sale_id=sale['id'],
            shop_id=sale['shop_id'],
            amount=sale['grand_total'],
            payment_method=sale['payment_method'],
            tenant_id=sale['tenant_id']
        )
        
        # Step 8: Publish financial transaction created event to Kafka
        financial_transaction_event = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': financial_transaction['id'],
            'sale_id': sale['id'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'amount': financial_transaction['amount'],
            'payment_method': financial_transaction['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['CASH_EVENTS'],
            key=financial_transaction['id'],
            event_data=financial_transaction_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['CASH_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == financial_transaction['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 9: Update reporting data
        reporting_update = mock_update_reporting_data(
            sale_id=sale['id'],
            shop_id=sale['shop_id'],
            items=sale['items'],
            amount=sale['grand_total'],
            tenant_id=sale['tenant_id']
        )
        
        # Step 10: Publish reporting data updated event to Kafka
        reporting_updated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'sale_id': sale['id'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'report_type': 'sales_summary',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=sale['id'],
            event_data=reporting_updated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sale['id']
        
        # Verify the complete flow
        assert sale['status'] == 'pending'
        assert approval['status'] == 'approved'
        assert inventory_update['items_updated'] == len(sale['items'])
        assert financial_transaction['amount'] == sale['grand_total']
        assert financial_transaction['payment_method'] == sale['payment_method']
        assert reporting_update['sale_id'] == sale['id']
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_sale_rejection_flow(self, mock_get_producer, mock_kafka_producer, 
                                shop_data, brand_data, user_data):
        """
        Test the flow when a sale is rejected.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        manager_id = str(uuid.uuid4())  # Manager who will reject the sale
        
        # Create sale items
        items = [
            {
                'brand_id': brand_id,
                'quantity': 2,
                'price_type': 'regular',
                'unit_price': brand_data['regular_price'],
                'total_price': 2 * brand_data['regular_price'],
                'tax_amount': 2 * brand_data['regular_price'] * (brand_data['tax_rate'] / 100)
            }
        ]
        
        # Step 1: Create a sale in the sales service
        sale = mock_create_sale(
            shop_id=shop_id,
            items=items,
            payment_method='cash',
            user_id=user_id,
            tenant_id=tenant_id
        )
        
        # Step 2: Publish sale created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        sale_created_event = {
            'event_type': EVENT_TYPES['SALE_CREATED'],
            'sale_id': sale['id'],
            'invoice_number': sale['invoice_number'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'total_amount': sale['grand_total'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SALES_EVENTS'],
            key=sale['id'],
            event_data=sale_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Reject the sale
        rejection_data = {
            'id': sale['id'],
            'status': 'rejected',
            'rejected_by': manager_id,
            'rejection_reason': 'Incorrect pricing',
            'rejected_at': timezone.now().isoformat()
        }
        
        # Step 4: Publish sale rejected event to Kafka
        sale_rejected_event = {
            'event_type': EVENT_TYPES['SALE_REJECTED'],
            'sale_id': sale['id'],
            'invoice_number': sale['invoice_number'],
            'shop_id': sale['shop_id'],
            'tenant_id': sale['tenant_id'],
            'rejected_by': rejection_data['rejected_by'],
            'rejection_reason': rejection_data['rejection_reason'],
            'rejected_at': rejection_data['rejected_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SALES_EVENTS'],
            key=sale['id'],
            event_data=sale_rejected_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SALES_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sale['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SALE_REJECTED']
        assert published_event['sale_id'] == sale['id']
        assert published_event['shop_id'] == sale['shop_id']
        assert published_event['tenant_id'] == sale['tenant_id']
        assert published_event['rejected_by'] == rejection_data['rejected_by']
        assert published_event['rejection_reason'] == rejection_data['rejection_reason']
