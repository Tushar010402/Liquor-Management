import json
import logging
import time
from confluent_kafka import Producer, Consumer, KafkaError
import os

logger = logging.getLogger(__name__)

# Default Kafka configuration for testing
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def get_kafka_producer():
    """
    Create and return a Kafka producer instance.
    """
    try:
        config = {
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'client.id': 'test_producer',
            'acks': 'all',  # Wait for all replicas to acknowledge
            'retries': 3,   # Retry up to 3 times
            'retry.backoff.ms': 500,  # 0.5 seconds between retries
        }
        
        return Producer(config)
    except Exception as e:
        logger.error(f"Error creating Kafka producer: {str(e)}")
        return None

def get_kafka_consumer(consumer_group, topics):
    """
    Create and return a Kafka consumer instance.
    
    Args:
        consumer_group (str): Consumer group ID
        topics (list): List of topics to subscribe to
    """
    try:
        config = {
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        }
        
        consumer = Consumer(config)
        consumer.subscribe(topics)
        
        return consumer
    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {str(e)}")
        return None

def publish_event(topic, key, event_data):
    """
    Publish an event to a Kafka topic.
    
    Args:
        topic (str): Kafka topic
        key (str): Event key
        event_data (dict): Event data
    """
    producer = get_kafka_producer()
    
    if not producer:
        logger.error("Failed to get Kafka producer")
        return False
    
    try:
        # Convert value to JSON string
        value = json.dumps(event_data).encode('utf-8')
        
        # Produce message
        producer.produce(
            topic=topic,
            key=key.encode('utf-8') if key else None,
            value=value,
            callback=delivery_report
        )
        
        # Wait for any outstanding messages to be delivered
        producer.flush()
        
        logger.info(f"Published event to {topic}: {key}")
        return True
        
    except Exception as e:
        logger.error(f"Error publishing event to {topic}: {str(e)}")
        return False

def delivery_report(err, msg):
    """
    Callback function for Kafka producer to report delivery status.
    """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def consume_events(consumer_group, topics, process_message, timeout=5.0, max_messages=10):
    """
    Consume events from Kafka topics and process them.
    
    Args:
        consumer_group (str): Consumer group ID
        topics (list): List of topics to subscribe to
        process_message (callable): Function to process messages
        timeout (float): Maximum time to wait for messages in seconds
        max_messages (int): Maximum number of messages to consume
    """
    consumer = get_kafka_consumer(consumer_group, topics)
    
    if not consumer:
        logger.error("Failed to get Kafka consumer")
        return
    
    try:
        messages_consumed = 0
        start_time = time.time()
        
        while messages_consumed < max_messages and (time.time() - start_time) < timeout:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
                
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.debug(f"Reached end of partition {msg.topic()} [{msg.partition()}]")
                else:
                    logger.error(f"Error consuming message: {msg.error()}")
                continue
                
            # Process message
            try:
                key = msg.key().decode('utf-8') if msg.key() else None
                value = json.loads(msg.value().decode('utf-8'))
                
                # Call the process_message function
                process_message(key, value)
                messages_consumed += 1
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in message: {msg.value()}")
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
    finally:
        # Close the consumer
        consumer.close()
