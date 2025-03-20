import json
import logging
from confluent_kafka import Producer, Consumer, KafkaError
from django.conf import settings

logger = logging.getLogger(__name__)

def get_kafka_producer():
    """
    Create and return a Kafka producer instance.
    """
    config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'auth_service_producer',
        'acks': 'all',  # Wait for all replicas to acknowledge
        'retries': 3,   # Retry up to 3 times
        'retry.backoff.ms': 500,  # 0.5 seconds between retries
    }
    
    return Producer(config)

def get_kafka_consumer(group_id, topics):
    """
    Create and return a Kafka consumer instance.
    
    Args:
        group_id (str): Consumer group ID
        topics (list): List of topics to subscribe to
    """
    config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    }
    
    consumer = Consumer(config)
    consumer.subscribe(topics)
    
    return consumer

def publish_event(topic, key, value):
    """
    Publish an event to a Kafka topic.
    
    Args:
        topic (str): Kafka topic
        key (str): Event key
        value (dict): Event data
    """
    producer = get_kafka_producer()
    
    try:
        # Convert value to JSON string
        value_json = json.dumps(value).encode('utf-8')
        
        # Produce message
        producer.produce(
            topic=topic,
            key=key.encode('utf-8') if key else None,
            value=value_json,
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
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def consume_events(consumer, timeout=1.0, max_messages=100):
    """
    Consume events from Kafka topics.
    
    Args:
        consumer: Kafka consumer instance
        timeout (float): Timeout in seconds
        max_messages (int): Maximum number of messages to consume
        
    Returns:
        list: List of consumed messages
    """
    messages = []
    
    try:
        for _ in range(max_messages):
            msg = consumer.poll(timeout)
            
            if msg is None:
                break
                
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.debug(f"Reached end of partition {msg.topic()} [{msg.partition()}]")
                else:
                    logger.error(f"Error consuming message: {msg.error()}")
                continue
                
            # Process message
            try:
                value = json.loads(msg.value().decode('utf-8'))
                messages.append({
                    'topic': msg.topic(),
                    'partition': msg.partition(),
                    'offset': msg.offset(),
                    'key': msg.key().decode('utf-8') if msg.key() else None,
                    'value': value
                })
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in message: {msg.value()}")
                
        # Commit offsets
        consumer.commit()
        
    except Exception as e:
        logger.error(f"Error consuming events: {str(e)}")
        
    return messages