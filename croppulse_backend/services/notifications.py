"""
Notification Service for CropPulse Africa
Handles push notifications via Firebase Cloud Messaging
"""
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending push notifications via Firebase"""
    
    def __init__(self):
        self.initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if settings.FIREBASE_CREDENTIALS_PATH and not self.initialized:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                self.initialized = True
                logger.info('Firebase initialized successfully')
        except Exception as e:
            logger.warning(f'Firebase initialization failed: {str(e)}')
            self.initialized = False
    
    def send_push_notification(
        self,
        device_token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> bool:
        """
        Send push notification to a single device
        
        Args:
            device_token: FCM device token
            title: Notification title
            body: Notification body
            data: Additional data payload
            
        Returns:
            bool: True if sent successfully
        """
        if not self.initialized:
            logger.error('Firebase not initialized')
            return False
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=device_token,
            )
            
            response = messaging.send(message)
            logger.info(f'Push notification sent: {response}')
            return True
            
        except Exception as e:
            logger.error(f'Failed to send push notification: {str(e)}')
            return False
    
    def send_multicast_notification(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Send push notification to multiple devices
        
        Args:
            device_tokens: List of FCM device tokens
            title: Notification title
            body: Notification body
            data: Additional data payload
            
        Returns:
            dict: Results with success and failure counts
        """
        if not self.initialized:
            logger.error('Firebase not initialized')
            return {'success_count': 0, 'failure_count': len(device_tokens)}
        
        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                tokens=device_tokens,
            )
            
            response = messaging.send_multicast(message)
            
            logger.info(
                f'Multicast sent. Success: {response.success_count}, '
                f'Failure: {response.failure_count}'
            )
            
            return {
                'success_count': response.success_count,
                'failure_count': response.failure_count,
                'responses': response.responses,
            }
            
        except Exception as e:
            logger.error(f'Failed to send multicast notification: {str(e)}')
            return {
                'success_count': 0,
                'failure_count': len(device_tokens),
                'error': str(e),
            }
    
    def send_topic_notification(
        self,
        topic: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> bool:
        """
        Send notification to a topic (all subscribed devices)
        
        Args:
            topic: Topic name
            title: Notification title
            body: Notification body
            data: Additional data payload
            
        Returns:
            bool: True if sent successfully
        """
        if not self.initialized:
            logger.error('Firebase not initialized')
            return False
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                topic=topic,
            )
            
            response = messaging.send(message)
            logger.info(f'Topic notification sent to {topic}: {response}')
            return True
            
        except Exception as e:
            logger.error(f'Failed to send topic notification: {str(e)}')
            return False
    
    def subscribe_to_topic(self, device_tokens: List[str], topic: str) -> Dict:
        """
        Subscribe devices to a topic
        
        Args:
            device_tokens: List of device tokens
            topic: Topic name
            
        Returns:
            dict: Subscription results
        """
        if not self.initialized:
            logger.error('Firebase not initialized')
            return {'success_count': 0, 'failure_count': len(device_tokens)}
        
        try:
            response = messaging.subscribe_to_topic(device_tokens, topic)
            
            logger.info(
                f'Subscribed to topic {topic}. Success: {response.success_count}, '
                f'Failure: {response.failure_count}'
            )
            
            return {
                'success_count': response.success_count,
                'failure_count': response.failure_count,
            }
            
        except Exception as e:
            logger.error(f'Failed to subscribe to topic: {str(e)}')
            return {
                'success_count': 0,
                'failure_count': len(device_tokens),
                'error': str(e),
            }
    
    def unsubscribe_from_topic(self, device_tokens: List[str], topic: str) -> Dict:
        """
        Unsubscribe devices from a topic
        
        Args:
            device_tokens: List of device tokens
            topic: Topic name
            
        Returns:
            dict: Unsubscription results
        """
        if not self.initialized:
            logger.error('Firebase not initialized')
            return {'success_count': 0, 'failure_count': len(device_tokens)}
        
        try:
            response = messaging.unsubscribe_from_topic(device_tokens, topic)
            
            logger.info(
                f'Unsubscribed from topic {topic}. Success: {response.success_count}, '
                f'Failure: {response.failure_count}'
            )
            
            return {
                'success_count': response.success_count,
                'failure_count': response.failure_count,
            }
            
        except Exception as e:
            logger.error(f'Failed to unsubscribe from topic: {str(e)}')
            return {
                'success_count': 0,
                'failure_count': len(device_tokens),
                'error': str(e),
            }


# Singleton instance
notification_service = NotificationService()
