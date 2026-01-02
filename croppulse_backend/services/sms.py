"""
SMS Service with Console Logging for Development
File: services/sms.py (update your existing file)
"""
import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS messages via Twilio with console fallback"""
    
    def __init__(self):
        # Check if Twilio credentials are configured
        self.use_twilio = all([
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_PHONE_NUMBER,
        ])
        
        if self.use_twilio:
            try:
                self.client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
                logger.info("✅ Twilio SMS client initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Twilio: {e}")
                self.use_twilio = False
        else:
            logger.warning("⚠️ Twilio not configured - using console mode")
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS to phone number
        In development without Twilio: logs to console
        In production with Twilio: sends real SMS
        
        Args:
            phone_number: Phone in E.164 format (+254...)
            message: SMS content
            
        Returns:
            bool: True if sent successfully
        """
        # DEVELOPMENT MODE: Log to console
        if settings.DEBUG and not self.use_twilio:
            logger.warning("\n" + "=" * 70)
            logger.warning("📱 SMS CONSOLE OUTPUT (Development Mode)")
            logger.warning("=" * 70)
            logger.warning(f"TO: {phone_number}")
            logger.warning(f"MESSAGE: {message}")
            logger.warning("=" * 70 + "\n")
            
            # Also print to console for visibility
            print("\n" + "=" * 70)
            print("📱 SMS SENT (Console Mode)")
            print("=" * 70)
            print(f"TO: {phone_number}")
            print(f"MESSAGE: {message}")
            print("=" * 70 + "\n")
            
            return True
        
        # PRODUCTION MODE: Send via Twilio
        try:
            response = self.client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            logger.info(f"✅ SMS sent to {phone_number}. SID: {response.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"❌ Twilio error sending to {phone_number}: {e.msg}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to send SMS to {phone_number}: {str(e)}")
            return False
    
    def send_verification_code(self, phone_number: str, code: str) -> bool:
        """
        Send verification code via SMS
        
        Args:
            phone_number: Phone in E.164 format
            code: Verification code
            
        Returns:
            bool: True if sent successfully
        """
        message = f"Your CropPulse verification code is: {code}. Valid for 10 minutes."
        return self.send_sms(phone_number, message)
    
    def send_alert(self, phone_number: str, alert_message: str) -> bool:
        """
        Send weather alert via SMS
        
        Args:
            phone_number: Phone in E.164 format
            alert_message: Alert content
            
        Returns:
            bool: True if sent successfully
        """
        message = f"CropPulse Alert: {alert_message}"
        return self.send_sms(phone_number, message)


# Singleton instance
sms_service = SMSService()