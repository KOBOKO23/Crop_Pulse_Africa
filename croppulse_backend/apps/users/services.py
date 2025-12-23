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
        Generate and send verification code to user
        
        Args:
            user: User instance
            
        Returns:
            bool: True if sent successfully
        """
        # Generate new code
        user.verification_code = generate_verification_code()
        user.verification_code_created_at = timezone.now()
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
        """
        Send OTP for passwordless login (farmers only)
        
        Args:
            user: User instance
            
        Returns:
            bool: True if sent successfully
        """
        # Generate new OTP code
        user.verification_code = generate_verification_code()
        user.verification_code_created_at = timezone.now()
        user.save(update_fields=['verification_code', 'verification_code_created_at'])
        
        # Send via SMS
        message = f'Your CropPulse Africa login code is: {user.verification_code}. Valid for 10 minutes.'
        success = sms_service.send_sms(str(user.phone_number), message)
        
        logger.info(f'Login OTP sent to {user.phone_number}: {success}')
        return success
    
    @staticmethod
    def get_onboarding_status(user: User) -> Dict:
        """
        Check user's onboarding completion status
        
        Args:
            user: User instance
            
        Returns:
            dict: Onboarding status information
        """
        next_steps = []
        
        # Check basic requirements
        has_profile_picture = bool(user.profile_picture)
        has_location = bool(user.county)
        is_verified = user.is_verified
        
        # Check role-specific requirements
        has_farm_details = False
        if user.role == 'farmer' and hasattr(user, 'farmer_profile'):
            profile = user.farmer_profile
            has_farm_details = bool(
                profile.farm_name and 
                profile.farm_size > 0 and
                profile.latitude and 
                profile.longitude
            )
            
            if not has_farm_details:
                next_steps.append('Complete farm details (name, size, location)')
        
        # Build next steps list
        if not is_verified:
            next_steps.insert(0, 'Verify your phone number')
        if not has_profile_picture:
            next_steps.append('Add a profile picture')
        if not has_location:
            next_steps.append('Set your location (county/subcounty)')
        
        # Check if onboarding is complete
        if user.role == 'farmer':
            onboarding_complete = (
                is_verified and 
                has_location and 
                has_farm_details
            )
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
        Get simplified dashboard data for farmers
        
        Args:
            user: Farmer user instance
            
        Returns:
            dict: Dashboard data
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
        
        # Get farm details
        if hasattr(user, 'farmer_profile'):
            profile = user.farmer_profile
            data['farm'] = {
                'name': profile.farm_name,
                'size': float(profile.farm_size) if profile.farm_size else 0,
                'primary_crop': profile.primary_crop,
                'has_coordinates': bool(profile.latitude and profile.longitude)
            }
        
        # Get active alerts for user's county
        if user.county:
            now = timezone.now()
            active_alerts = Alert.objects.filter(
                status='active',
                counties__contains=[user.county],
                start_time__lte=now,
                end_time__gte=now
            ).count()
            data['active_alerts'] = active_alerts
            
            # Get most recent weather data for county
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
        
        # Get unread notifications count
        from .models import Notification
        data['unread_notifications'] = Notification.objects.filter(
            user=user,
            is_read=False
        ).count()
        
        return data
    
    @staticmethod
    def get_field_officer_dashboard_data(user: User) -> Dict:
        """
        Get dashboard data for field officers
        
        Args:
            user: Field officer user instance
            
        Returns:
            dict: Dashboard data
        """
        from apps.observations.models import FarmObservation
        from apps.alerts.models import Alert
        
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
        
        # Get field officer details
        if hasattr(user, 'field_officer_profile'):
            profile = user.field_officer_profile
            data['user']['employee_id'] = profile.employee_id
            data['user']['assigned_areas'] = profile.assigned_counties
        
        # Get pending observations for verification
        data['pending_verifications'] = FarmObservation.objects.filter(
            status='pending',
            county__in=data['user']['assigned_areas'] if data['user']['assigned_areas'] else [user.county]
        ).count()
        
        # Get active alerts
        now = timezone.now()
        data['active_alerts'] = Alert.objects.filter(
            status='active',
            start_time__lte=now,
            end_time__gte=now
        ).count()
        
        # Get today's observations
        from datetime import date
        data['observations_today'] = FarmObservation.objects.filter(
            created_at__date=date.today()
        ).count()
        
        return data
    
    @staticmethod
    def create_notification(
        user: User,
        notification_type: str,
        title: str,
        message: str,
        priority: str = 'medium',
        data: dict = None,
        send_push: bool = True,
        send_sms: bool = False
    ) -> Notification:
        """
        Create a notification for a user
        
        Args:
            user: User instance
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            priority: Priority level
            data: Additional data
            send_push: Whether to send push notification
            send_sms: Whether to send SMS
            
        Returns:
            Notification instance
        """
        notification = Notification.objects.create(
            user=user,
            type=notification_type,
            priority=priority,
            title=title,
            message=message,
            data=data or {}
        )
        
        # Send push notification
        if send_push and user.receive_push_notifications and user.fcm_token:
            try:
                notification_service.send_push_notification(
                    user.fcm_token,
                    title,
                    message,
                    data
                )
                notification.sent_via_push = True
                notification.save(update_fields=['sent_via_push'])
            except Exception as e:
                logger.error(f'Failed to send push notification: {str(e)}')
        
        # Send SMS
        if send_sms and user.receive_sms_notifications:
            try:
                sms_service.send_sms(
                    str(user.phone_number),
                    f"{title}: {message}"
                )
                notification.sent_via_sms = True
                notification.save(update_fields=['sent_via_sms'])
            except Exception as e:
                logger.error(f'Failed to send SMS: {str(e)}')
        
        return notification
    
    @staticmethod
    def bulk_create_notifications(
        users: List[User],
        notification_type: str,
        title: str,
        message: str,
        priority: str = 'medium',
        data: dict = None,
        send_push: bool = True,
        send_sms: bool = False
    ) -> int:
        """
        Create notifications for multiple users
        
        Returns:
            int: Number of notifications created
        """
        notifications = []
        push_tokens = []
        sms_numbers = []
        
        for user in users:
            notification = Notification(
                user=user,
                type=notification_type,
                priority=priority,
                title=title,
                message=message,
                data=data or {}
            )
            notifications.append(notification)
            
            if send_push and user.receive_push_notifications and user.fcm_token:
                push_tokens.append(user.fcm_token)
            
            if send_sms and user.receive_sms_notifications:
                sms_numbers.append(str(user.phone_number))
        
        # Bulk create notifications
        created = Notification.objects.bulk_create(notifications)
        
        # Send push notifications
        if push_tokens:
            try:
                notification_service.send_multicast_notification(
                    push_tokens,
                    title,
                    message,
                    data
                )
            except Exception as e:
                logger.error(f'Failed to send multicast push: {str(e)}')
        
        # Send SMS
        if sms_numbers:
            try:
                sms_service.send_bulk_sms(
                    sms_numbers,
                    f"{title}: {message}"
                )
            except Exception as e:
                logger.error(f'Failed to send bulk SMS: {str(e)}')
        
        return len(created)
    
    @staticmethod
    def get_users_in_area(
        latitude: float,
        longitude: float,
        radius_km: float,
        role: Optional[str] = None
    ) -> List[User]:
        """
        Get users within a radius of coordinates
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_km: Radius in kilometers
            role: Optional role filter
            
        Returns:
            List of User instances
        """
        from core.utils import calculate_distance
        
        # Get all users with coordinates (farmers)
        query = Q(farmer_profile__latitude__isnull=False)
        
        if role:
            query &= Q(role=role)
        
        users = User.objects.filter(query).select_related('farmer_profile')
        
        # Filter by distance
        nearby_users = []
        for user in users:
            if hasattr(user, 'farmer_profile'):
                profile = user.farmer_profile
                if profile.latitude and profile.longitude:
                    distance = calculate_distance(
                        latitude, longitude,
                        float(profile.latitude), float(profile.longitude)
                    )
                    if distance <= radius_km:
                        nearby_users.append(user)
        
        return nearby_users
    
    @staticmethod
    def get_users_by_county(county: str, role: Optional[str] = None) -> List[User]:
        """
        Get users in a specific county
        
        Args:
            county: County name
            role: Optional role filter
            
        Returns:
            List of User instances
        """
        query = Q(county__iexact=county)
        
        if role:
            query &= Q(role=role)
        
        return list(User.objects.filter(query))
    
    @staticmethod
    def cleanup_old_notifications(days: int = 30) -> int:
        """
        Delete read notifications older than specified days
        
        Args:
            days: Number of days
            
        Returns:
            int: Number of notifications deleted
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        deleted_count, _ = Notification.objects.filter(
            is_read=True,
            created_at__lt=cutoff_date
        ).delete()
        
        return deleted_count