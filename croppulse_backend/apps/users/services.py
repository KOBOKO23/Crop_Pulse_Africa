"""
Business logic services for Users app
"""
from django.utils import timezone
from django.db.models import Q
from typing import List, Optional, Dict
from .models import User, Notification
from core.utils import generate_verification_code
from services.sms import sms_service
from services.notifications import notification_service
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def send_verification_code(user: User) -> bool:
        """
        Generate and send verification code to user.
        Reuses existing code if it is still valid (<10 mins).
        """
        now = timezone.now()
        code_expired = True

        if user.verification_code_created_at:
            elapsed = now - user.verification_code_created_at
            if elapsed.total_seconds() < 600:  # 10 minutes
                code_expired = False

        if code_expired or not user.verification_code:
            user.verification_code = generate_verification_code()
            user.verification_code_created_at = now
            user.save(update_fields=['verification_code', 'verification_code_created_at'])

        # Send via SMS
        success = sms_service.send_verification_code(
            str(user.phone_number),
            user.verification_code
        )

        logger.info(f'Verification code sent to {user.phone_number}: {success}')
        return success

    @staticmethod
    def send_login_otp(user: User) -> bool:
        """Send OTP for passwordless login"""
        from django.utils import timezone
        from core.utils import generate_verification_code
        from services.sms import sms_service
        import logging
        
        logger = logging.getLogger(__name__)
        
        now = timezone.now()
        code_expired = True

        # Check if existing OTP is still valid
        if user.verification_code_created_at:
            elapsed = now - user.verification_code_created_at
            if elapsed.total_seconds() < 600:  # 10 minutes
                code_expired = False
                logger.info(f"♻️ Reusing valid OTP for {user.phone_number}")

        # Generate new OTP if needed
        if code_expired or not user.verification_code:
            user.verification_code = generate_verification_code()
            user.verification_code_created_at = now
            user.save(update_fields=['verification_code', 'verification_code_created_at'])
            logger.info(f"🆕 Generated new OTP for {user.phone_number}")

        # Send SMS
        message = f'Your CropPulse Africa login code is: {user.verification_code}. Valid for 10 minutes.'
        success = sms_service.send_sms(str(user.phone_number), message)

        logger.info(f"📤 OTP: {user.verification_code} - SMS sent: {success}")
        
        return success

    @staticmethod
    def get_onboarding_status(user: User) -> Dict:
        """
        Check user's onboarding completion status.
        """
        next_steps = []

        has_profile_picture = bool(user.profile_picture)
        has_location = bool(user.county)
        is_verified = user.is_verified
        has_farm_details = False

        if user.role == 'farmer' and hasattr(user, 'farmer_profile'):
            profile = user.farmer_profile
            has_farm_details = bool(
                profile.farm_name and 
                profile.farm_size > 0 and
                profile.latitude is not None and 
                profile.longitude is not None
            )
            if not has_farm_details:
                next_steps.append('Complete farm details (name, size, location)')

        if not is_verified:
            next_steps.insert(0, 'Verify your phone number')
        if not has_profile_picture:
            next_steps.append('Add a profile picture')
        if not has_location:
            next_steps.append('Set your location (county/subcounty)')

        if user.role == 'farmer':
            onboarding_complete = is_verified and has_location and has_farm_details
        elif user.role == 'field_officer':
            onboarding_complete = is_verified and has_location
        else:
            onboarding_complete = is_verified

        return {
            'has_profile_picture': has_profile_picture,
            'has_location': has_location,
            'has_farm_details': has_farm_details,
            'is_verified': is_verified,
            'onboarding_complete': onboarding_complete,
            'next_steps': next_steps
        }

    @staticmethod
    def get_farmer_dashboard_data(user: User) -> Dict:
        """
        Get simplified dashboard data for farmers.
        """
        from apps.alerts.models import Alert
        from apps.weather.models import WeatherData

        data = {
            'user': {
                'full_name': user.full_name,
                'county': user.county,
                'language': user.language,
            },
            'farm': None,
            'active_alerts': 0,
            'recent_weather': None,
            'unread_notifications': 0,
        }

        if hasattr(user, 'farmer_profile'):
            profile = user.farmer_profile
            data['farm'] = {
                'name': profile.farm_name,
                'size': float(profile.farm_size or 0),
                'primary_crop': profile.primary_crop,
                'has_coordinates': bool(profile.latitude and profile.longitude)
            }

        if user.county:
            now = timezone.now()
            data['active_alerts'] = Alert.objects.filter(
                status='active',
                counties__contains=[user.county],
                start_time__lte=now,
                end_time__gte=now
            ).count()

            recent_weather = WeatherData.objects.filter(
                county__iexact=user.county
            ).order_by('-recorded_at').first()

            if recent_weather:
                data['recent_weather'] = {
                    'temperature': float(recent_weather.temperature),
                    'condition': recent_weather.condition,
                    'rainfall': float(recent_weather.rainfall),
                    'recorded_at': recent_weather.recorded_at.isoformat()
                }

        data['unread_notifications'] = Notification.objects.filter(
            user=user,
            is_read=False
        ).count()

        return data

    @staticmethod
    def get_field_officer_dashboard_data(user: User) -> Dict:
        """
        Get dashboard data for field officers.
        """
        from apps.observations.models import FarmObservation
        from apps.alerts.models import Alert
        from datetime import date

        data = {
            'user': {
                'full_name': user.full_name,
                'employee_id': None,
                'assigned_areas': [],
            },
            'pending_verifications': 0,
            'active_alerts': 0,
            'observations_today': 0,
        }

        if hasattr(user, 'field_officer_profile'):
            profile = user.field_officer_profile
            data['user']['employee_id'] = profile.employee_id
            data['user']['assigned_areas'] = profile.assigned_counties

        assigned_areas = data['user']['assigned_areas'] or [user.county]

        data['pending_verifications'] = FarmObservation.objects.filter(
            status='pending',
            county__in=assigned_areas
        ).count()

        now = timezone.now()
        data['active_alerts'] = Alert.objects.filter(
            status='active',
            start_time__lte=now,
            end_time__gte=now
        ).count()

        data['observations_today'] = FarmObservation.objects.filter(
            created_at__date=date.today()
        ).count()

        return data
