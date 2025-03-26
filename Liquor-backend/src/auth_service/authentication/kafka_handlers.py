import logging
import json
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)
User = get_user_model()

def start_kafka_consumers():
    """
    Start Kafka consumers for the auth service.
    """
    logger.info("Starting Kafka consumers for auth service")
    
    # Start consumer for user events
    try:
        consume_events(
            CONSUMER_GROUPS['AUTH_SERVICE'],
            [TOPICS['USER_EVENTS']],
            process_user_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for user events: {str(e)}")

def process_user_event(key, event_data):
    """
    Process user events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['USER_CREATED']:
            logger.info(f"Processing user created event: {key}")
            # This is handled by the auth service directly
            pass
        
        elif event_type == EVENT_TYPES['USER_UPDATED']:
            logger.info(f"Processing user updated event: {key}")
            # This is handled by the auth service directly
            pass
        
        elif event_type == EVENT_TYPES['USER_LOGIN']:
            logger.info(f"Processing user login event: {key}")
            # Update user's last login time if needed
            user_id = event_data.get('user_id')
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if user:
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
        
        elif event_type == EVENT_TYPES['USER_LOGOUT']:
            logger.info(f"Processing user logout event: {key}")
            # This is handled by the auth service directly
            pass
        
        else:
            logger.warning(f"Unknown event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing user event: {str(e)}")

def publish_user_created_event(user):
    """
    Publish a user created event to Kafka.
    
    Args:
        user: User object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['USER_CREATED'],
            'user_id': str(user.id),
            'email': user.email,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'role': user.role.name if hasattr(user, 'role') and user.role else None,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['USER_EVENTS'], f'user:{user.id}', event_data)
        logger.info(f"Published user created event for user {user.id}")
    
    except Exception as e:
        logger.error(f"Error publishing user created event: {str(e)}")

def publish_user_updated_event(user, updated_fields):
    """
    Publish a user updated event to Kafka.
    
    Args:
        user: User object.
        updated_fields: List of updated fields.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['USER_UPDATED'],
            'user_id': str(user.id),
            'email': user.email,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'updated_fields': updated_fields,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['USER_EVENTS'], f'user:{user.id}', event_data)
        logger.info(f"Published user updated event for user {user.id}")
    
    except Exception as e:
        logger.error(f"Error publishing user updated event: {str(e)}")

def publish_user_login_event(user):
    """
    Publish a user login event to Kafka.
    
    Args:
        user: User object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['USER_LOGIN'],
            'user_id': str(user.id),
            'email': user.email,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['USER_EVENTS'], f'user:{user.id}', event_data)
        logger.info(f"Published user login event for user {user.id}")
    
    except Exception as e:
        logger.error(f"Error publishing user login event: {str(e)}")

def publish_user_logout_event(user):
    """
    Publish a user logout event to Kafka.
    
    Args:
        user: User object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['USER_LOGOUT'],
            'user_id': str(user.id),
            'email': user.email,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['USER_EVENTS'], f'user:{user.id}', event_data)
        logger.info(f"Published user logout event for user {user.id}")
    
    except Exception as e:
        logger.error(f"Error publishing user logout event: {str(e)}")