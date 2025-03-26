"""
Performance tests for Kafka throughput in the Liquor Management System.
These tests measure the Kafka performance under load, including producer throughput,
consumer throughput, message latency, and batch processing.
"""

import time
import uuid
import json
import pytest
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import BOOTSTRAP_SERVERS, TOPICS, EVENT_TYPES
from common.utils.kafka_utils import get_kafka_producer, get_kafka_consumer

# Test configuration
NUM_THREADS = 10
NUM_MESSAGES = 1000
BATCH_SIZE = 100
TEST_TOPIC = "performance_test_topic"

class TestKafkaProducerPerformance:
    """
    Test the performance of Kafka producers under load.
    """
    
    @pytest.fixture(scope="class")
    def setup_test_topic(self):
        """Set up a test topic for performance testing."""
        from kafka.admin import KafkaAdminClient, NewTopic
        
        # Create admin client
        admin_client = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            client_id='test-admin'
        )
        
        # Check if topic exists
        try:
            topics = admin_client.list_topics()
            if TEST_TOPIC not in topics:
                # Create test topic
                topic_list = [
                    NewTopic(
                        name=TEST_TOPIC,
                        num_partitions=3,
                        replication_factor=1
                    )
                ]
                admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except Exception as e:
            print(f"Error creating test topic: {e}")
        finally:
            admin_client.close()
    
    def test_single_producer_throughput(self, setup_test_topic):
        """Test the throughput of a single Kafka producer."""
        # Get Kafka producer
        producer = get_kafka_producer()
        
        # Generate test messages
        test_messages = [
            {
                'id': str(uuid.uuid4()),
                'event_type': 'TEST_EVENT',
                'data': {
                    'field1': f'value{i}',
                    'field2': i,
                    'timestamp': timezone.now().isoformat()
                }
            }
            for i in range(NUM_MESSAGES)
        ]
        
        # Measure time to send messages
        start_time = time.time()
        
        for message in test_messages:
            producer.send(
                TEST_TOPIC,
                key=message['id'].encode('utf-8'),
                value=json.dumps(message).encode('utf-8')
            )
        
        # Ensure all messages are sent
        producer.flush()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate throughput
        throughput = NUM_MESSAGES / total_time
        
        print(f"\nSingle Producer Throughput:")
        print(f"Total messages: {NUM_MESSAGES}")
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Messages per second: {throughput:.2f}")
        
        # Assert performance criteria
        assert throughput > 100, f"Single producer throughput ({throughput:.2f} msgs/sec) below threshold (100 msgs/sec)"
    
    def test_multi_producer_throughput(self, setup_test_topic):
        """Test the throughput of multiple Kafka producers running in parallel."""
        # Function to execute in threads
        def producer_task(message_batch):
            producer = get_kafka_producer()
            
            for message in message_batch:
                producer.send(
                    TEST_TOPIC,
                    key=message['id'].encode('utf-8'),
                    value=json.dumps(message).encode('utf-8')
                )
            
            producer.flush()
            producer.close()
        
        # Generate test messages
        test_messages = [
            {
                'id': str(uuid.uuid4()),
                'event_type': 'TEST_EVENT',
                'data': {
                    'field1': f'value{i}',
                    'field2': i,
                    'timestamp': timezone.now().isoformat()
                }
            }
            for i in range(NUM_MESSAGES)
        ]
        
        # Split messages into batches for each thread
        batch_size = NUM_MESSAGES // NUM_THREADS
        message_batches = [
            test_messages[i:i+batch_size]
            for i in range(0, NUM_MESSAGES, batch_size)
        ]
        
        # Measure time to send messages in parallel
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(producer_task, message_batches)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate throughput
        throughput = NUM_MESSAGES / total_time
        
        print(f"\nMulti-Producer Throughput ({NUM_THREADS} producers):")
        print(f"Total messages: {NUM_MESSAGES}")
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Messages per second: {throughput:.2f}")
        
        # Assert performance criteria
        assert throughput > 500, f"Multi-producer throughput ({throughput:.2f} msgs/sec) below threshold (500 msgs/sec)"
    
    def test_batch_producer_throughput(self, setup_test_topic):
        """Test the throughput of batch message production."""
        # Get Kafka producer with batch settings
        from kafka import KafkaProducer
        
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            batch_size=16384,  # 16KB batch size
            linger_ms=10,      # 10ms linger time
            acks='all'
        )
        
        # Generate test messages
        test_messages = [
            {
                'id': str(uuid.uuid4()),
                'event_type': 'TEST_EVENT',
                'data': {
                    'field1': f'value{i}',
                    'field2': i,
                    'timestamp': timezone.now().isoformat()
                }
            }
            for i in range(NUM_MESSAGES)
        ]
        
        # Measure time to send messages in batches
        start_time = time.time()
        
        for message in test_messages:
            producer.send(
                TEST_TOPIC,
                key=message['id'],
                value=message
            )
        
        # Ensure all messages are sent
        producer.flush()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate throughput
        throughput = NUM_MESSAGES / total_time
        
        print(f"\nBatch Producer Throughput:")
        print(f"Total messages: {NUM_MESSAGES}")
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Messages per second: {throughput:.2f}")
        
        # Assert performance criteria
        assert throughput > 1000, f"Batch producer throughput ({throughput:.2f} msgs/sec) below threshold (1000 msgs/sec)"

class TestKafkaConsumerPerformance:
    """
    Test the performance of Kafka consumers under load.
    """
    
    @pytest.fixture(scope="class")
    def setup_test_data(self, setup_test_topic):
        """Set up test data for consumer performance testing."""
        # Get Kafka producer
        producer = get_kafka_producer()
        
        # Generate and send test messages
        test_messages = [
            {
                'id': str(uuid.uuid4()),
                'event_type': 'TEST_EVENT',
                'data': {
                    'field1': f'value{i}',
                    'field2': i,
                    'timestamp': timezone.now().isoformat()
                }
            }
            for i in range(NUM_MESSAGES)
        ]
        
        for message in test_messages:
            producer.send(
                TEST_TOPIC,
                key=message['id'].encode('utf-8'),
                value=json.dumps(message).encode('utf-8')
            )
        
        # Ensure all messages are sent
        producer.flush()
        
        return test_messages
    
    def test_single_consumer_throughput(self, setup_test_data):
        """Test the throughput of a single Kafka consumer."""
        # Get Kafka consumer
        consumer = get_kafka_consumer(
            group_id=f'test-consumer-{uuid.uuid4()}',
            auto_offset_reset='earliest'
        )
        
        # Subscribe to test topic
        consumer.subscribe([TEST_TOPIC])
        
        # Measure time to consume messages
        start_time = time.time()
        message_count = 0
        
        # Set a timeout to avoid infinite loop
        timeout = time.time() + 60  # 60 seconds timeout
        
        while message_count < NUM_MESSAGES and time.time() < timeout:
            # Poll for messages
            messages = consumer.poll(timeout_ms=1000, max_records=100)
            
            # Process messages
            for partition, records in messages.items():
                message_count += len(records)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Close consumer
        consumer.close()
        
        # Calculate throughput
        throughput = message_count / total_time
        
        print(f"\nSingle Consumer Throughput:")
        print(f"Total messages consumed: {message_count}")
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Messages per second: {throughput:.2f}")
        
        # Assert performance criteria
        assert throughput > 100, f"Single consumer throughput ({throughput:.2f} msgs/sec) below threshold (100 msgs/sec)"
    
    def test_consumer_group_throughput(self, setup_test_data):
        """Test the throughput of a consumer group with multiple consumers."""
        # Function to execute in threads
        def consumer_task(results, consumer_id):
            # Get Kafka consumer
            consumer = get_kafka_consumer(
                group_id=f'test-group-{uuid.uuid4()}',
                auto_offset_reset='earliest'
            )
            
            # Subscribe to test topic
            consumer.subscribe([TEST_TOPIC])
            
            # Consume messages
            message_count = 0
            start_time = time.time()
            
            # Set a timeout to avoid infinite loop
            timeout = time.time() + 60  # 60 seconds timeout
            
            while time.time() < timeout:
                # Poll for messages
                messages = consumer.poll(timeout_ms=1000, max_records=100)
                
                # Process messages
                for partition, records in messages.items():
                    message_count += len(records)
                
                # Break if we've consumed enough messages
                if message_count >= NUM_MESSAGES // NUM_THREADS:
                    break
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Close consumer
            consumer.close()
            
            # Store results
            results[consumer_id] = {
                'message_count': message_count,
                'total_time': total_time
            }
        
        # Create shared results dictionary
        results = {}
        
        # Create and start consumer threads
        threads = []
        for i in range(NUM_THREADS):
            thread = threading.Thread(
                target=consumer_task,
                args=(results, i)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Calculate total messages consumed and average throughput
        total_messages = sum(result['message_count'] for result in results.values())
        total_time = max(result['total_time'] for result in results.values())
        
        # Calculate throughput
        throughput = total_messages / total_time
        
        print(f"\nConsumer Group Throughput ({NUM_THREADS} consumers):")
        print(f"Total messages consumed: {total_messages}")
        print(f"Total time: {total_time:.6f} seconds")
        print(f"Messages per second: {throughput:.2f}")
        
        # Assert performance criteria
        assert throughput > 500, f"Consumer group throughput ({throughput:.2f} msgs/sec) below threshold (500 msgs/sec)"

class TestKafkaLatencyPerformance:
    """
    Test the message latency of Kafka under load.
    """
    
    def test_end_to_end_latency(self, setup_test_topic):
        """Test the end-to-end latency of Kafka messages."""
        # Get Kafka producer and consumer
        producer = get_kafka_producer()
        
        consumer = get_kafka_consumer(
            group_id=f'latency-test-{uuid.uuid4()}',
            auto_offset_reset='latest'
        )
        
        # Subscribe to test topic
        consumer.subscribe([TEST_TOPIC])
        
        # Consume any existing messages to start from a clean state
        consumer.poll(timeout_ms=1000)
        
        # Generate test messages with timestamps
        latencies = []
        
        for i in range(100):  # Use a smaller number for latency testing
            # Create message with current timestamp
            message_id = str(uuid.uuid4())
            send_time = time.time()
            
            message = {
                'id': message_id,
                'event_type': 'LATENCY_TEST',
                'send_time': send_time,
                'data': {
                    'test_value': i
                }
            }
            
            # Send message
            producer.send(
                TEST_TOPIC,
                key=message_id.encode('utf-8'),
                value=json.dumps(message).encode('utf-8')
            )
            
            # Ensure message is sent immediately
            producer.flush()
            
            # Poll for the message
            received = False
            start_poll_time = time.time()
            
            while not received and time.time() - start_poll_time < 10:  # 10 second timeout
                messages = consumer.poll(timeout_ms=100)
                
                for partition, records in messages.items():
                    for record in records:
                        record_value = json.loads(record.value.decode('utf-8'))
                        
                        if record_value.get('id') == message_id:
                            receive_time = time.time()
                            latency = receive_time - record_value['send_time']
                            latencies.append(latency)
                            received = True
                            break
                    
                    if received:
                        break
        
        # Calculate latency statistics
        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        
        print(f"\nEnd-to-End Latency:")
        print(f"Average latency: {avg_latency * 1000:.2f} ms")
        print(f"Max latency: {max_latency * 1000:.2f} ms")
        print(f"Min latency: {min_latency * 1000:.2f} ms")
        print(f"95th percentile: {p95_latency * 1000:.2f} ms")
        
        # Assert performance criteria
        assert avg_latency < 0.1, f"Average latency ({avg_latency * 1000:.2f} ms) exceeds threshold (100 ms)"
        assert p95_latency < 0.2, f"95th percentile latency ({p95_latency * 1000:.2f} ms) exceeds threshold (200 ms)"

class TestKafkaScalabilityPerformance:
    """
    Test the scalability of Kafka under increasing load.
    """
    
    @pytest.mark.parametrize("num_partitions", [1, 3, 6])
    def test_partition_scalability(self, num_partitions):
        """Test the scalability of Kafka with different partition counts."""
        from kafka.admin import KafkaAdminClient, NewTopic
        
        # Create a unique topic for this test
        test_topic = f"scalability_test_topic_{num_partitions}_{uuid.uuid4().hex[:8]}"
        
        # Create admin client
        admin_client = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            client_id='test-admin'
        )
        
        try:
            # Create test topic with specified partitions
            topic_list = [
                NewTopic(
                    name=test_topic,
                    num_partitions=num_partitions,
                    replication_factor=1
                )
            ]
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            
            # Get Kafka producer
            producer = get_kafka_producer()
            
            # Generate test messages
            test_messages = [
                {
                    'id': str(uuid.uuid4()),
                    'event_type': 'TEST_EVENT',
                    'data': {
                        'field1': f'value{i}',
                        'field2': i,
                        'timestamp': timezone.now().isoformat()
                    }
                }
                for i in range(NUM_MESSAGES)
            ]
            
            # Measure time to send messages
            start_time = time.time()
            
            for message in test_messages:
                producer.send(
                    test_topic,
                    key=message['id'].encode('utf-8'),
                    value=json.dumps(message).encode('utf-8')
                )
            
            # Ensure all messages are sent
            producer.flush()
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Calculate throughput
            throughput = NUM_MESSAGES / total_time
            
            print(f"\nPartition Scalability ({num_partitions} partitions):")
            print(f"Total messages: {NUM_MESSAGES}")
            print(f"Total time: {total_time:.6f} seconds")
            print(f"Messages per second: {throughput:.2f}")
            
            return throughput
            
        finally:
            # Clean up - delete test topic
            try:
                admin_client.delete_topics([test_topic])
            except Exception as e:
                print(f"Error deleting test topic: {e}")
            finally:
                admin_client.close()
    
    @pytest.mark.parametrize("message_size", [100, 1000, 10000])
    def test_message_size_impact(self, message_size):
        """Test the impact of message size on Kafka performance."""
        # Create a unique topic for this test
        test_topic = f"message_size_test_topic_{message_size}_{uuid.uuid4().hex[:8]}"
        
        # Create admin client
        from kafka.admin import KafkaAdminClient, NewTopic
        
        admin_client = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            client_id='test-admin'
        )
        
        try:
            # Create test topic
            topic_list = [
                NewTopic(
                    name=test_topic,
                    num_partitions=3,
                    replication_factor=1
                )
            ]
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            
            # Get Kafka producer
            producer = get_kafka_producer()
            
            # Generate test messages with specified size
            test_messages = [
                {
                    'id': str(uuid.uuid4()),
                    'event_type': 'TEST_EVENT',
                    'data': {
                        'field1': 'x' * message_size,  # Create string of specified size
                        'timestamp': timezone.now().isoformat()
                    }
                }
                for i in range(100)  # Use fewer messages for large sizes
            ]
            
            # Measure time to send messages
            start_time = time.time()
            
            for message in test_messages:
                producer.send(
                    test_topic,
                    key=message['id'].encode('utf-8'),
                    value=json.dumps(message).encode('utf-8')
                )
            
            # Ensure all messages are sent
            producer.flush()
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Calculate throughput
            throughput = 100 / total_time
            
            print(f"\nMessage Size Impact ({message_size} bytes):")
            print(f"Total messages: 100")
            print(f"Total time: {total_time:.6f} seconds")
            print(f"Messages per second: {throughput:.2f}")
            
            return throughput
            
        finally:
            # Clean up - delete test topic
            try:
                admin_client.delete_topics([test_topic])
            except Exception as e:
                print(f"Error deleting test topic: {e}")
            finally:
                admin_client.close()
