import json
import unittest
from unittest.mock import patch, MagicMock, call
from django.test import TestCase
from common.utils.kafka_utils import (
    get_kafka_producer, get_kafka_consumer,
    publish_event, consume_events, delivery_report
)

class KafkaUtilsTest(TestCase):
    """
    Test the Kafka utilities.
    """
    
    @patch('common.utils.kafka_utils.Producer')
    def test_get_kafka_producer(self, mock_producer):
        """
        Test get_kafka_producer function.
        """
        # Mock the Producer
        mock_producer_instance = MagicMock()
        mock_producer.return_value = mock_producer_instance
        
        # Call the function
        producer = get_kafka_producer()
        
        # Assertions
        self.assertEqual(producer, mock_producer_instance)
        mock_producer.assert_called_once()
    
    @patch('common.utils.kafka_utils.Producer')
    def test_get_kafka_producer_exception(self, mock_producer):
        """
        Test get_kafka_producer function with exception.
        """
        # Mock the Producer to raise an exception
        mock_producer.side_effect = Exception('Connection error')
        
        # Call the function
        producer = get_kafka_producer()
        
        # Assertions
        self.assertIsNone(producer)
        mock_producer.assert_called_once()
    
    @patch('common.utils.kafka_utils.Consumer')
    def test_get_kafka_consumer(self, mock_consumer):
        """
        Test get_kafka_consumer function.
        """
        # Mock the Consumer
        mock_consumer_instance = MagicMock()
        mock_consumer.return_value = mock_consumer_instance
        
        # Call the function
        consumer = get_kafka_consumer('test-group', ['test-topic'])
        
        # Assertions
        self.assertEqual(consumer, mock_consumer_instance)
        mock_consumer.assert_called_once()
        mock_consumer_instance.subscribe.assert_called_once_with(['test-topic'])
    
    @patch('common.utils.kafka_utils.Consumer')
    def test_get_kafka_consumer_exception(self, mock_consumer):
        """
        Test get_kafka_consumer function with exception.
        """
        # Mock the Consumer to raise an exception
        mock_consumer.side_effect = Exception('Connection error')
        
        # Call the function
        consumer = get_kafka_consumer('test-group', ['test-topic'])
        
        # Assertions
        self.assertIsNone(consumer)
        mock_consumer.assert_called_once()
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_publish_event(self, mock_get_producer):
        """
        Test publish_event function.
        """
        # Mock the producer
        mock_producer = MagicMock()
        mock_get_producer.return_value = mock_producer
        
        # Test data
        topic = 'test-topic'
        key = 'test-key'
        event_data = {'event_type': 'test_event', 'data': 'test_data'}
        
        # Call the function
        result = publish_event(topic, key, event_data)
        
        # Assertions
        self.assertTrue(result)
        mock_get_producer.assert_called_once()
        mock_producer.produce.assert_called_once()
        mock_producer.flush.assert_called_once()
        
        # Check the produce call arguments
        args, kwargs = mock_producer.produce.call_args
        self.assertEqual(kwargs['topic'], topic)
        self.assertEqual(kwargs['key'], key.encode('utf-8'))
        self.assertEqual(json.loads(kwargs['value'].decode('utf-8')), event_data)
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_publish_event_no_producer(self, mock_get_producer):
        """
        Test publish_event function with no producer.
        """
        # Mock the producer to return None
        mock_get_producer.return_value = None
        
        # Test data
        topic = 'test-topic'
        key = 'test-key'
        event_data = {'event_type': 'test_event', 'data': 'test_data'}
        
        # Call the function
        result = publish_event(topic, key, event_data)
        
        # Assertions
        self.assertFalse(result)
        mock_get_producer.assert_called_once()
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_publish_event_exception(self, mock_get_producer):
        """
        Test publish_event function with exception.
        """
        # Mock the producer to raise an exception
        mock_producer = MagicMock()
        mock_producer.produce.side_effect = Exception('Produce error')
        mock_get_producer.return_value = mock_producer
        
        # Test data
        topic = 'test-topic'
        key = 'test-key'
        event_data = {'event_type': 'test_event', 'data': 'test_data'}
        
        # Call the function
        result = publish_event(topic, key, event_data)
        
        # Assertions
        self.assertFalse(result)
        mock_get_producer.assert_called_once()
        mock_producer.produce.assert_called_once()
    
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_consume_events(self, mock_get_consumer):
        """
        Test consume_events function.
        """
        # Mock the consumer
        mock_consumer = MagicMock()
        mock_get_consumer.return_value = mock_consumer
        
        # Mock the poll method to return a message and then raise KeyboardInterrupt
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = b'test-key'
        mock_message.value.return_value = json.dumps({'event_type': 'test_event', 'data': 'test_data'}).encode('utf-8')
        
        mock_consumer.poll.side_effect = [
            mock_message,  # First call returns a message
            KeyboardInterrupt()  # Second call raises KeyboardInterrupt to stop the loop
        ]
        
        # Mock the process_message function
        mock_process_message = MagicMock()
        
        # Call the function
        consume_events('test-group', ['test-topic'], mock_process_message)
        
        # Assertions
        mock_get_consumer.assert_called_once_with('test-group', ['test-topic'])
        mock_consumer.poll.assert_called()
        mock_message.error.assert_called_once()
        mock_message.key.assert_called_once()
        mock_message.value.assert_called_once()
        mock_process_message.assert_called_once_with(
            'test-key',
            {'event_type': 'test_event', 'data': 'test_data'}
        )
        mock_consumer.close.assert_called_once()
    
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_consume_events_no_consumer(self, mock_get_consumer):
        """
        Test consume_events function with no consumer.
        """
        # Mock the consumer to return None
        mock_get_consumer.return_value = None
        
        # Mock the process_message function
        mock_process_message = MagicMock()
        
        # Call the function
        consume_events('test-group', ['test-topic'], mock_process_message)
        
        # Assertions
        mock_get_consumer.assert_called_once_with('test-group', ['test-topic'])
        mock_process_message.assert_not_called()
    
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_consume_events_message_error(self, mock_get_consumer):
        """
        Test consume_events function with message error.
        """
        # Mock the consumer
        mock_consumer = MagicMock()
        mock_get_consumer.return_value = mock_consumer
        
        # Mock the poll method to return a message with error and then raise KeyboardInterrupt
        mock_message = MagicMock()
        mock_error = MagicMock()
        mock_error.code.return_value = 1  # Some error code
        mock_message.error.return_value = mock_error
        
        mock_consumer.poll.side_effect = [
            mock_message,  # First call returns a message with error
            KeyboardInterrupt()  # Second call raises KeyboardInterrupt to stop the loop
        ]
        
        # Mock the process_message function
        mock_process_message = MagicMock()
        
        # Call the function
        consume_events('test-group', ['test-topic'], mock_process_message)
        
        # Assertions
        mock_get_consumer.assert_called_once_with('test-group', ['test-topic'])
        mock_consumer.poll.assert_called()
        mock_message.error.assert_called()
        mock_process_message.assert_not_called()
        mock_consumer.close.assert_called_once()
    
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_consume_events_process_exception(self, mock_get_consumer):
        """
        Test consume_events function with process_message exception.
        """
        # Mock the consumer
        mock_consumer = MagicMock()
        mock_get_consumer.return_value = mock_consumer
        
        # Mock the poll method to return a message and then raise KeyboardInterrupt
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = b'test-key'
        mock_message.value.return_value = json.dumps({'event_type': 'test_event', 'data': 'test_data'}).encode('utf-8')
        
        mock_consumer.poll.side_effect = [
            mock_message,  # First call returns a message
            KeyboardInterrupt()  # Second call raises KeyboardInterrupt to stop the loop
        ]
        
        # Mock the process_message function to raise an exception
        mock_process_message = MagicMock()
        mock_process_message.side_effect = Exception('Process error')
        
        # Call the function
        consume_events('test-group', ['test-topic'], mock_process_message)
        
        # Assertions
        mock_get_consumer.assert_called_once_with('test-group', ['test-topic'])
        mock_consumer.poll.assert_called()
        mock_message.error.assert_called_once()
        mock_message.key.assert_called_once()
        mock_message.value.assert_called_once()
        mock_process_message.assert_called_once()
        mock_consumer.close.assert_called_once()
    
    def test_delivery_report_success(self):
        """
        Test delivery_report function with success.
        """
        # Mock the message
        mock_message = MagicMock()
        mock_message.topic.return_value = 'test-topic'
        mock_message.partition.return_value = 0
        
        # Call the function
        with self.assertLogs(level='DEBUG') as cm:
            delivery_report(None, mock_message)
        
        # Assertions
        self.assertIn('Message delivered to test-topic [0]', cm.output[0])
    
    def test_delivery_report_error(self):
        """
        Test delivery_report function with error.
        """
        # Mock the error
        mock_error = Exception('Delivery error')
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            delivery_report(mock_error, None)
        
        # Assertions
        self.assertIn('Message delivery failed: Delivery error', cm.output[0])