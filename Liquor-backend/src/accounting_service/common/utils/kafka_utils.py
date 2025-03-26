import json
import logging
from django.conf import settings
from confluent_kafka import Producer, Consumer, KafkaError

logger = logging.getLogger(__name__)

def get_kafka_producer():
    """
    Get a Kafka producer instance.
    
    Returns:
        Producer: A Kafka producer instance.
    """
    try:
        producer_config = {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'client.id': 'accounting-service-producer'
        }
        return Producer(producer_config)
    except Exception as e:
        logger.error(f"Error creating Kafka producer: {str(e)}")
        return None

def get_kafka_consumer(group_id, topics):
    """
    Get a Kafka consumer instance.
    
    Args:
        group_id (str): Consumer group ID.
        topics (list): List of topics to subscribe to.
        
    Returns:
        Consumer: A Kafka consumer instance.
    """
    try:
        consumer_config = {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe(topics)
        return consumer
    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {str(e)}")
        return None

def publish_event(topic, key, event_data):
    """
    Publish an event to Kafka.
    
    Args:
        topic (str): Kafka topic.
        key (str): Event key.
        event_data (dict): Event data.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        producer = get_kafka_producer()
        if not producer:
            return False
        
        # Convert event data to JSON
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
        
        return True
    except Exception as e:
        logger.error(f"Error publishing event to Kafka: {str(e)}")
        return False

def consume_events(group_id, topics, process_message, poll_timeout=1.0):
    """
    Consume events from Kafka.
    
    Args:
        group_id (str): Consumer group ID.
        topics (list): List of topics to subscribe to.
        process_message (callable): Function to process messages.
        poll_timeout (float): Poll timeout in seconds.
        
    Returns:
        None
    """
    try:
        consumer = get_kafka_consumer(group_id, topics)
        if not consumer:
            return
        
        while True:
            msg = consumer.poll(poll_timeout)
            
            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.info(f"Reached end of partition {msg.partition()}")
                else:
                    # Error
                    logger.error(f"Error consuming message: {msg.error()}")
            else:
                # Process message
                try:
                    key = msg.key().decode('utf-8') if msg.key() else None
                    value = json.loads(msg.value().decode('utf-8'))
                    process_message(key, value)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
    except KeyboardInterrupt:
        logger.info("Stopping Kafka consumer")
    finally:
        if consumer:
            consumer.close()

def delivery_report(err, msg):
    """
    Delivery report callback for Kafka producer.
    
    Args:
        err: Error object or None.
        msg: Message object.
        
    Returns:
        None
    """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")