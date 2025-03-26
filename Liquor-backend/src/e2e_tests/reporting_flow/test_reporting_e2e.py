"""
End-to-end test for the reporting flow in the Liquor Management System.
This test verifies the complete flow of reporting processes, including sales reports,
inventory reports, financial reports, and dashboard data.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES

# Mock functions for the reporting flow
def mock_generate_sales_report(shop_id, tenant_id, start_date, end_date, report_type):
    """Mock function for generating a sales report in the reporting service."""
    report_id = str(uuid.uuid4())
    
    # Generate sample sales data
    sales_data = [
        {
            'date': (datetime.now() - timedelta(days=i)).date().isoformat(),
            'total_sales': 1000.0 - (i * 50),
            'total_items': 20 - i,
            'average_sale': (1000.0 - (i * 50)) / (20 - i)
        }
        for i in range(5)
    ]
    
    return {
        'id': report_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'start_date': start_date,
        'end_date': end_date,
        'report_type': report_type,
        'data': sales_data,
        'total_sales': sum(item['total_sales'] for item in sales_data),
        'total_items': sum(item['total_items'] for item in sales_data),
        'status': 'generated',
        'created_at': timezone.now().isoformat()
    }

def mock_generate_inventory_report(shop_id, tenant_id, report_type):
    """Mock function for generating an inventory report in the reporting service."""
    report_id = str(uuid.uuid4())
    
    # Generate sample inventory data
    inventory_data = [
        {
            'brand_id': str(uuid.uuid4()),
            'brand_name': f'Brand {i+1}',
            'category': 'whisky',
            'current_stock': 50 - (i * 5),
            'min_level': 10,
            'max_level': 100,
            'value': (50 - (i * 5)) * 400.0
        }
        for i in range(5)
    ]
    
    return {
        'id': report_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'report_type': report_type,
        'data': inventory_data,
        'total_items': len(inventory_data),
        'total_value': sum(item['value'] for item in inventory_data),
        'status': 'generated',
        'created_at': timezone.now().isoformat()
    }

def mock_generate_financial_report(shop_id, tenant_id, start_date, end_date, report_type):
    """Mock function for generating a financial report in the reporting service."""
    report_id = str(uuid.uuid4())
    
    # Generate sample financial data
    financial_data = {
        'revenue': {
            'sales': 50000.0,
            'other': 1000.0,
            'total': 51000.0
        },
        'expenses': {
            'purchases': 30000.0,
            'salaries': 10000.0,
            'rent': 5000.0,
            'utilities': 2000.0,
            'other': 1000.0,
            'total': 48000.0
        },
        'profit': 3000.0,
        'profit_margin': (3000.0 / 51000.0) * 100
    }
    
    return {
        'id': report_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'start_date': start_date,
        'end_date': end_date,
        'report_type': report_type,
        'data': financial_data,
        'status': 'generated',
        'created_at': timezone.now().isoformat()
    }

def mock_generate_dashboard_data(shop_id, tenant_id):
    """Mock function for generating dashboard data in the reporting service."""
    dashboard_id = str(uuid.uuid4())
    
    # Generate sample dashboard data
    dashboard_data = {
        'sales_summary': {
            'today': 2000.0,
            'yesterday': 1800.0,
            'this_week': 12000.0,
            'last_week': 11500.0,
            'this_month': 45000.0,
            'last_month': 42000.0
        },
        'inventory_summary': {
            'total_items': 500,
            'low_stock_items': 15,
            'expiring_items': 10,
            'total_value': 200000.0
        },
        'financial_summary': {
            'revenue_this_month': 45000.0,
            'expenses_this_month': 40000.0,
            'profit_this_month': 5000.0,
            'profit_margin': 11.11
        },
        'top_selling_brands': [
            {'brand_id': str(uuid.uuid4()), 'brand_name': 'Brand 1', 'quantity': 50, 'amount': 20000.0},
            {'brand_id': str(uuid.uuid4()), 'brand_name': 'Brand 2', 'quantity': 40, 'amount': 16000.0},
            {'brand_id': str(uuid.uuid4()), 'brand_name': 'Brand 3', 'quantity': 30, 'amount': 12000.0},
            {'brand_id': str(uuid.uuid4()), 'brand_name': 'Brand 4', 'quantity': 20, 'amount': 8000.0},
            {'brand_id': str(uuid.uuid4()), 'brand_name': 'Brand 5', 'quantity': 10, 'amount': 4000.0}
        ]
    }
    
    return {
        'id': dashboard_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'data': dashboard_data,
        'generated_at': timezone.now().isoformat()
    }

class TestReportingE2EFlow:
    """
    Test the end-to-end reporting flow in the Liquor Management System.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_sales_report_generation_flow(self, mock_get_consumer, mock_get_producer,
                                         mock_kafka_producer, mock_kafka_consumer,
                                         shop_data, tenant_data):
        """
        Test the complete flow of generating a sales report, from request to delivery.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
        end_date = datetime.now().date().isoformat()
        report_type = 'sales_summary'
        
        # Step 1: Create a report request
        report_request_id = str(uuid.uuid4())
        report_request = {
            'id': report_request_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'start_date': start_date,
            'end_date': end_date,
            'report_type': report_type,
            'parameters': {
                'format': 'pdf',
                'include_charts': True
            },
            'status': 'scheduled',
            'created_at': timezone.now().isoformat()
        }
        
        # Step 2: Publish report request event to Kafka
        from common.utils.kafka_utils import publish_event
        
        report_request_event = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'report_id': report_request['id'],
            'shop_id': report_request['shop_id'],
            'tenant_id': report_request['tenant_id'],
            'report_type': report_request['report_type'],
            'parameters': report_request['parameters'],
            'start_date': report_request['start_date'],
            'end_date': report_request['end_date'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_request['id'],
            event_data=report_request_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_request['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Generate the sales report
        sales_report = mock_generate_sales_report(
            shop_id=report_request['shop_id'],
            tenant_id=report_request['tenant_id'],
            start_date=report_request['start_date'],
            end_date=report_request['end_date'],
            report_type=report_request['report_type']
        )
        
        # Step 4: Publish report generated event to Kafka
        report_generated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': sales_report['id'],
            'shop_id': sales_report['shop_id'],
            'tenant_id': sales_report['tenant_id'],
            'report_type': sales_report['report_type'],
            'file_url': f'/reports/{sales_report["id"]}.pdf',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=sales_report['id'],
            event_data=report_generated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sales_report['id']
        
        # Verify the sales report
        assert sales_report['status'] == 'generated'
        assert sales_report['report_type'] == report_type
        assert sales_report['start_date'] == start_date
        assert sales_report['end_date'] == end_date
        assert len(sales_report['data']) == 5
        assert 'total_sales' in sales_report
        assert 'total_items' in sales_report
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_inventory_report_generation_flow(self, mock_get_consumer, mock_get_producer,
                                            mock_kafka_producer, mock_kafka_consumer,
                                            shop_data, tenant_data):
        """
        Test the complete flow of generating an inventory report, from request to delivery.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        report_type = 'inventory_status'
        
        # Step 1: Create a report request
        report_request_id = str(uuid.uuid4())
        report_request = {
            'id': report_request_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'report_type': report_type,
            'parameters': {
                'format': 'pdf',
                'include_charts': True
            },
            'status': 'scheduled',
            'created_at': timezone.now().isoformat()
        }
        
        # Step 2: Publish report request event to Kafka
        from common.utils.kafka_utils import publish_event
        
        report_request_event = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'report_id': report_request['id'],
            'shop_id': report_request['shop_id'],
            'tenant_id': report_request['tenant_id'],
            'report_type': report_request['report_type'],
            'parameters': report_request['parameters'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_request['id'],
            event_data=report_request_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_request['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Generate the inventory report
        inventory_report = mock_generate_inventory_report(
            shop_id=report_request['shop_id'],
            tenant_id=report_request['tenant_id'],
            report_type=report_request['report_type']
        )
        
        # Step 4: Publish report generated event to Kafka
        report_generated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': inventory_report['id'],
            'shop_id': inventory_report['shop_id'],
            'tenant_id': inventory_report['tenant_id'],
            'report_type': inventory_report['report_type'],
            'file_url': f'/reports/{inventory_report["id"]}.pdf',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=inventory_report['id'],
            event_data=report_generated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == inventory_report['id']
        
        # Verify the inventory report
        assert inventory_report['status'] == 'generated'
        assert inventory_report['report_type'] == report_type
        assert len(inventory_report['data']) == 5
        assert 'total_items' in inventory_report
        assert 'total_value' in inventory_report
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_financial_report_generation_flow(self, mock_get_consumer, mock_get_producer,
                                            mock_kafka_producer, mock_kafka_consumer,
                                            shop_data, tenant_data):
        """
        Test the complete flow of generating a financial report, from request to delivery.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
        end_date = datetime.now().date().isoformat()
        report_type = 'profit_and_loss'
        
        # Step 1: Create a report request
        report_request_id = str(uuid.uuid4())
        report_request = {
            'id': report_request_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'start_date': start_date,
            'end_date': end_date,
            'report_type': report_type,
            'parameters': {
                'format': 'pdf',
                'include_charts': True
            },
            'status': 'scheduled',
            'created_at': timezone.now().isoformat()
        }
        
        # Step 2: Publish report request event to Kafka
        from common.utils.kafka_utils import publish_event
        
        report_request_event = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'report_id': report_request['id'],
            'shop_id': report_request['shop_id'],
            'tenant_id': report_request['tenant_id'],
            'report_type': report_request['report_type'],
            'parameters': report_request['parameters'],
            'start_date': report_request['start_date'],
            'end_date': report_request['end_date'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_request['id'],
            event_data=report_request_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_request['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Generate the financial report
        financial_report = mock_generate_financial_report(
            shop_id=report_request['shop_id'],
            tenant_id=report_request['tenant_id'],
            start_date=report_request['start_date'],
            end_date=report_request['end_date'],
            report_type=report_request['report_type']
        )
        
        # Step 4: Publish report generated event to Kafka
        report_generated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': financial_report['id'],
            'shop_id': financial_report['shop_id'],
            'tenant_id': financial_report['tenant_id'],
            'report_type': financial_report['report_type'],
            'file_url': f'/reports/{financial_report["id"]}.pdf',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=financial_report['id'],
            event_data=report_generated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == financial_report['id']
        
        # Verify the financial report
        assert financial_report['status'] == 'generated'
        assert financial_report['report_type'] == report_type
        assert financial_report['start_date'] == start_date
        assert financial_report['end_date'] == end_date
        assert 'revenue' in financial_report['data']
        assert 'expenses' in financial_report['data']
        assert 'profit' in financial_report['data']
        assert 'profit_margin' in financial_report['data']
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_dashboard_data_generation_flow(self, mock_get_producer, mock_kafka_producer,
                                          shop_data, tenant_data):
        """
        Test the flow of generating dashboard data in the reporting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        
        # Step 1: Generate dashboard data
        dashboard_data = mock_generate_dashboard_data(
            shop_id=shop_id,
            tenant_id=tenant_id
        )
        
        # Step 2: Publish dashboard data generated event to Kafka
        from common.utils.kafka_utils import publish_event
        
        dashboard_event = {
            'event_type': EVENT_TYPES['DASHBOARD_DATA_UPDATED'],
            'dashboard_id': dashboard_data['id'],
            'shop_id': dashboard_data['shop_id'],
            'tenant_id': dashboard_data['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=dashboard_data['id'],
            event_data=dashboard_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == dashboard_data['id']
        
        # Verify the dashboard data
        assert 'sales_summary' in dashboard_data['data']
        assert 'inventory_summary' in dashboard_data['data']
        assert 'financial_summary' in dashboard_data['data']
        assert 'top_selling_brands' in dashboard_data['data']
        assert len(dashboard_data['data']['top_selling_brands']) == 5
