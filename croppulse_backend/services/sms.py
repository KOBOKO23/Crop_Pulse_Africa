"""
SMS Service for CropPulse Africa
Integrates with Twilio for SMS notifications
"""
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from core.exceptions import SMSServiceError
from core.utils import format_phone_number
import logging

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS notifications via Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_PHONE_NUMBER
        
        if all([self.account_sid, self.auth_token, self.from_number]):
            self.client = Client(self.account_sid, self.auth_token)
        else:
            logger.warning('Twilio credentials not configured')
            self.client = None
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """
        Send SMS to a phone number
        
        Args:
            to_number: Recipient phone number
            message: Message content
            
        Returns:
            bool: True if sent successfully
        """
        if not self.client:
            logger.error('SMS service not configured')
            return False
        
        try:
            # Format phone number
            formatted_number = format_phone_number(to_number)
            
            # Send SMS
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=formatted_number
            )
            
            logger.info(f'SMS sent successfully. SID: {message_obj.sid}')
            return True
            
        except TwilioRestException as e:
            logger.error(f'Twilio error: {str(e)}')
            raise SMSServiceError(f'Failed to send SMS: {str(e)}')
        except Exception as e:
            logger.error(f'SMS send error: {str(e)}')
            return False
    
    def send_bulk_sms(self, phone_numbers: list, message: str) -> dict:
        """
        Send SMS to multiple recipients
        
        Args:
            phone_numbers: List of recipient phone numbers
            message: Message content
            
        Returns:
            dict: Results with successful and failed sends
        """
        results = {
            'successful': [],
            'failed': [],
        }
        
        for number in phone_numbers:
            try:
                success = self.send_sms(number, message)
                if success:
                    results['successful'].append(number)
                else:
                    results['failed'].append(number)
            except Exception as e:
                logger.error(f'Failed to send to {number}: {str(e)}')
                results['failed'].append(number)
        
        return results
    
    def send_verification_code(self, phone_number: str, code: str) -> bool:
        """
        Send verification code via SMS
        
        Args:
            phone_number: Recipient phone number
            code: Verification code
            
        Returns:
            bool: True if sent successfully
        """
        message = f'Your CropPulse Africa verification code is: {code}. Valid for 10 minutes.'
        return self.send_sms(phone_number, message)
    
    def send_alert_notification(self, phone_number: str, alert_title: str, alert_message: str) -> bool:
        """
        Send alert notification via SMS
        
        Args:
            phone_number: Recipient phone number
            alert_title: Alert title
            alert_message: Alert message
            
        Returns:
            bool: True if sent successfully
        """
        message = f'ALERT: {alert_title}\n{alert_message}\n- CropPulse Africa'
        return self.send_sms(phone_number, message)
    
    def send_weather_advisory(self, phone_number: str, advisory: str) -> bool:
        """
        Send weather advisory via SMS
        
        Args:
            phone_number: Recipient phone number
            advisory: Advisory message
            
        Returns:
            bool: True if sent successfully
        """
        message = f'Weather Advisory:\n{advisory}\n- CropPulse Africa'
        return self.send_sms(phone_number, message)
    
    def check_sms_status(self, message_sid: str) -> dict:
        """
        Check the status of a sent SMS
        
        Args:
            message_sid: Twilio message SID
            
        Returns:
            dict: Message status information
        """
        if not self.client:
            return {'status': 'unknown'}
        
        try:
            message = self.client.messages(message_sid).fetch()
            return {
                'sid': message.sid,
                'status': message.status,
                'to': message.to,
                'from': message.from_,
                'date_sent': message.date_sent,
                'error_code': message.error_code,
                'error_message': message.error_message,
            }
        except TwilioRestException as e:
            logger.error(f'Error checking SMS status: {str(e)}')
            return {'status': 'error', 'error': str(e)}


# Singleton instance
sms_service = SMSService()
