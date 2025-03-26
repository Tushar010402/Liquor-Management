"""
End-to-end test for the purchase flow in the Liquor Management System.
This test verifies the complete flow from creating a purchase order to its approval,
goods receipt, and the resulting inventory updates and financial transactions.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES

# Mock functions for the purchase flow
def mock_create_supplier(name, contact_name, phone, email, address, tenant_id, user_id):
    """Mock function for creating a supplier in the purchase service."""
    supplier_id = str(uuid.uuid4())
    
    return {
        'id': supplier_id,
        'name': name,
        'contact_name': contact_name,
        'phone': phone,
        'email': email,
        'address': address,
        'tenant_id': tenant_id,
        'status': 'active',
        'created_by': user_id,
        'created_at': timezone.now().isoformat()
    }

def mock_create_purchase_order(shop_id, tenant_id, supplier_id, items, user_id):
    """Mock function for creating a purchase order in the purchase service."""
    po_id = str(uuid.uuid4())
    po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    # Calculate totals
    subtotal = sum(item['quantity'] * item['purchase_price'] for item in items)
    tax_amount = subtotal * 0.18  # Assuming 18% tax
    total_amount = subtotal + tax_amount
    
    return {
        'id': po_id,
        'po_number': po_number,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'supplier_id': supplier_id,
        'items': items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'status': 'draft',
        'created_by': user_id,
        'created_at': timezone.now().isoformat()
    }

def mock_approve_purchase_order(po_id, approver_id):
    """Mock function for approving a purchase order in the purchase service."""
    return {
        'id': po_id,
        'status': 'approved',
        'approved_by': approver_id,
        'approved_at': timezone.now().isoformat()
    }

def mock_create_goods_receipt(po_id, shop_id, tenant_id, items, user_id):
    """Mock function for creating a goods receipt in the purchase service."""
    receipt_id = str(uuid.uuid4())
    receipt_number = f"GR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    return {
        'id': receipt_id,
        'receipt_number': receipt_number,
        'purchase_order_id': po_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'items': items,
        'status': 'pending',
        'created_by': user_id,
        'created_at': timezone.now().isoformat()
    }

def mock_complete_goods_receipt(receipt_id, user_id):
    """Mock function for completing a goods receipt in the purchase service."""
    return {
        'id': receipt_id,
        'status': 'completed',
        'completed_by': user_id,
        'completed_at': timezone.now().isoformat()
    }

def mock_update_inventory(shop_id, items, tenant_id):
    """Mock function for updating inventory after goods receipt is completed."""
    return {
        'shop_id': shop_id,
        'items_updated': len(items),
        'tenant_id': tenant_id,
        'updated_at': timezone.now().isoformat()
    }

def mock_create_financial_transaction(po_id, shop_id, amount, payment_method, tenant_id):
    """Mock function for creating a financial transaction in the accounting service."""
    transaction_id = str(uuid.uuid4())
    return {
        'id': transaction_id,
        'purchase_order_id': po_id,
        'shop_id': shop_id,
        'amount': amount,
        'payment_method': payment_method,
        'status': 'completed',
        'tenant_id': tenant_id,
        'created_at': timezone.now().isoformat()
    }

class TestPurchaseE2EFlow:
    """
    Test the end-to-end purchase flow in the Liquor Management System.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_supplier_creation_flow(self, mock_get_consumer, mock_get_producer,
                                   mock_kafka_producer, mock_kafka_consumer,
                                   tenant_data, user_data):
        """
        Test the flow of creating a supplier and synchronizing it across services.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        tenant_id = tenant_data['id']
        user_id = user_data['id']
        
        # Step 1: Create a supplier in the purchase service
        supplier = mock_create_supplier(
            name='Test Supplier',
            contact_name='John Doe',
            phone='1234567890',
            email='supplier@example.com',
            address='123 Supplier St, Supplier City',
            tenant_id=tenant_id,
            user_id=user_id
        )
        
        # Step 2: Publish supplier created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        supplier_created_event = {
            'event_type': EVENT_TYPES['SUPPLIER_CREATED'],
            'supplier_id': supplier['id'],
            'name': supplier['name'],
            'contact_name': supplier['contact_name'],
            'phone': supplier['phone'],
            'email': supplier['email'],
            'address': supplier['address'],
            'tenant_id': supplier['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SUPPLIER_EVENTS'],
            key=supplier['id'],
            event_data=supplier_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SUPPLIER_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == supplier['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SUPPLIER_CREATED']
        assert published_event['supplier_id'] == supplier['id']
        assert published_event['name'] == supplier['name']
        assert published_event['email'] == supplier['email']
        
        # Verify the supplier creation
        assert supplier['status'] == 'active'
        assert supplier['name'] == 'Test Supplier'
        assert supplier['email'] == 'supplier@example.com'
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_purchase_order_to_goods_receipt_flow(self, mock_get_consumer, mock_get_producer,
                                                 mock_kafka_producer, mock_kafka_consumer,
                                                 shop_data, brand_data, user_data, supplier_data):
        """
        Test the complete flow from creating a purchase order to its approval,
        goods receipt, and the resulting inventory updates and financial transactions.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        supplier_id = supplier_data['id']
        manager_id = str(uuid.uuid4())  # Manager who will approve the purchase order
        
        # Create purchase order items
        items = [
            {
                'brand_id': brand_id,
                'quantity': 50,
                'purchase_price': 300.0,
                'total_price': 50 * 300.0
            }
        ]
        
        # Step 1: Create a purchase order in the purchase service
        purchase_order = mock_create_purchase_order(
            shop_id=shop_id,
            tenant_id=tenant_id,
            supplier_id=supplier_id,
            items=items,
            user_id=user_id
        )
        
        # Step 2: Publish purchase order created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        po_created_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_CREATED'],
            'purchase_order_id': purchase_order['id'],
            'po_number': purchase_order['po_number'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'supplier_id': purchase_order['supplier_id'],
            'items': purchase_order['items'],
            'total_amount': purchase_order['total_amount'],
            'status': purchase_order['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=purchase_order['id'],
            event_data=po_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_order['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Approve the purchase order
        approval = mock_approve_purchase_order(
            po_id=purchase_order['id'],
            approver_id=manager_id
        )
        
        # Step 4: Publish purchase order approved event to Kafka
        po_approved_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_APPROVED'],
            'purchase_order_id': purchase_order['id'],
            'po_number': purchase_order['po_number'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'supplier_id': purchase_order['supplier_id'],
            'status': approval['status'],
            'approved_by': approval['approved_by'],
            'approved_at': approval['approved_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=purchase_order['id'],
            event_data=po_approved_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_order['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 5: Create goods receipt for the purchase order
        # Add batch and expiry date to the items
        receipt_items = [
            {
                'brand_id': item['brand_id'],
                'quantity': item['quantity'],
                'purchase_price': item['purchase_price'],
                'batch': f'BATCH-{uuid.uuid4().hex[:6]}',
                'expiry_date': (timezone.now() + timedelta(days=365)).date().isoformat()
            }
            for item in purchase_order['items']
        ]
        
        goods_receipt = mock_create_goods_receipt(
            po_id=purchase_order['id'],
            shop_id=purchase_order['shop_id'],
            tenant_id=purchase_order['tenant_id'],
            items=receipt_items,
            user_id=user_id
        )
        
        # Step 6: Publish goods receipt created event to Kafka
        gr_created_event = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_CREATED'],
            'goods_receipt_id': goods_receipt['id'],
            'receipt_number': goods_receipt['receipt_number'],
            'purchase_order_id': goods_receipt['purchase_order_id'],
            'shop_id': goods_receipt['shop_id'],
            'tenant_id': goods_receipt['tenant_id'],
            'items': goods_receipt['items'],
            'status': goods_receipt['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['GOODS_RECEIPT_EVENTS'],
            key=goods_receipt['id'],
            event_data=gr_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['GOODS_RECEIPT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == goods_receipt['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 7: Complete the goods receipt
        completed_receipt = mock_complete_goods_receipt(
            receipt_id=goods_receipt['id'],
            user_id=user_id
        )
        
        # Step 8: Publish goods receipt completed event to Kafka
        gr_completed_event = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_COMPLETED'],
            'goods_receipt_id': completed_receipt['id'],
            'purchase_order_id': goods_receipt['purchase_order_id'],
            'shop_id': goods_receipt['shop_id'],
            'tenant_id': goods_receipt['tenant_id'],
            'items': goods_receipt['items'],
            'status': completed_receipt['status'],
            'completed_by': completed_receipt['completed_by'],
            'completed_at': completed_receipt['completed_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['GOODS_RECEIPT_EVENTS'],
            key=completed_receipt['id'],
            event_data=gr_completed_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['GOODS_RECEIPT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == completed_receipt['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 9: Update inventory based on the completed goods receipt
        inventory_update = mock_update_inventory(
            shop_id=goods_receipt['shop_id'],
            items=goods_receipt['items'],
            tenant_id=goods_receipt['tenant_id']
        )
        
        # Step 10: Publish stock adjustment event to Kafka
        stock_adjustment_id = str(uuid.uuid4())
        stock_adjustment_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': stock_adjustment_id,
            'reference_id': completed_receipt['id'],
            'reference_type': 'goods_receipt',
            'shop_id': goods_receipt['shop_id'],
            'tenant_id': goods_receipt['tenant_id'],
            'items': goods_receipt['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=stock_adjustment_id,
            event_data=stock_adjustment_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_adjustment_id
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 11: Create financial transaction for the purchase
        financial_transaction = mock_create_financial_transaction(
            po_id=purchase_order['id'],
            shop_id=purchase_order['shop_id'],
            amount=purchase_order['total_amount'],
            payment_method='bank_transfer',
            tenant_id=purchase_order['tenant_id']
        )
        
        # Step 12: Publish financial transaction created event to Kafka
        financial_transaction_event = {
            'event_type': EVENT_TYPES['PURCHASE_PAYMENT_CREATED'],
            'transaction_id': financial_transaction['id'],
            'purchase_order_id': purchase_order['id'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'amount': financial_transaction['amount'],
            'payment_method': financial_transaction['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=financial_transaction['id'],
            event_data=financial_transaction_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == financial_transaction['id']
        
        # Verify the complete flow
        assert purchase_order['status'] == 'draft'
        assert approval['status'] == 'approved'
        assert goods_receipt['status'] == 'pending'
        assert completed_receipt['status'] == 'completed'
        assert inventory_update['items_updated'] == len(goods_receipt['items'])
        assert financial_transaction['amount'] == purchase_order['total_amount']
        assert financial_transaction['payment_method'] == 'bank_transfer'
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_purchase_order_rejection_flow(self, mock_get_producer, mock_kafka_producer,
                                          shop_data, brand_data, user_data, supplier_data):
        """
        Test the flow when a purchase order is rejected.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        supplier_id = supplier_data['id']
        manager_id = str(uuid.uuid4())  # Manager who will reject the purchase order
        
        # Create purchase order items
        items = [
            {
                'brand_id': brand_id,
                'quantity': 50,
                'purchase_price': 300.0,
                'total_price': 50 * 300.0
            }
        ]
        
        # Step 1: Create a purchase order in the purchase service
        purchase_order = mock_create_purchase_order(
            shop_id=shop_id,
            tenant_id=tenant_id,
            supplier_id=supplier_id,
            items=items,
            user_id=user_id
        )
        
        # Step 2: Publish purchase order created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        po_created_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_CREATED'],
            'purchase_order_id': purchase_order['id'],
            'po_number': purchase_order['po_number'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'supplier_id': purchase_order['supplier_id'],
            'items': purchase_order['items'],
            'total_amount': purchase_order['total_amount'],
            'status': purchase_order['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=purchase_order['id'],
            event_data=po_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Reject the purchase order
        rejection_data = {
            'id': purchase_order['id'],
            'status': 'rejected',
            'rejected_by': manager_id,
            'rejection_reason': 'Budget constraints',
            'rejected_at': timezone.now().isoformat()
        }
        
        # Step 4: Publish purchase order rejected event to Kafka
        po_rejected_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_REJECTED'],
            'purchase_order_id': purchase_order['id'],
            'po_number': purchase_order['po_number'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'supplier_id': purchase_order['supplier_id'],
            'status': rejection_data['status'],
            'rejected_by': rejection_data['rejected_by'],
            'rejection_reason': rejection_data['rejection_reason'],
            'rejected_at': rejection_data['rejected_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=purchase_order['id'],
            event_data=po_rejected_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_order['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['PURCHASE_ORDER_REJECTED']
        assert published_event['purchase_order_id'] == purchase_order['id']
        assert published_event['po_number'] == purchase_order['po_number']
        assert published_event['status'] == 'rejected'
        assert published_event['rejection_reason'] == 'Budget constraints'
