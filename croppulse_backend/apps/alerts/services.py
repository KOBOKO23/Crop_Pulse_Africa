"""
Business logic services for Alerts app
"""
from django.db.models import Q
from typing import List
from .models import Alert, AlertLog
from apps.users.models import User
from apps.users.services import UserService
from services.weather_api import weather_api
import logging

logger = logging.getLogger(__name__)


class AlertService:
    """Service class for alert-related operations"""
    
    @staticmethod
    def send_alert(alert: Alert) -> int:
        """
        Send alert to affected users
        
        Args:
            alert: Alert instance
            
        Returns:
            int: Number of users notified
        """
        # Get users in affected counties
        users = User.objects.filter(
            county__in=alert.counties,
            is_active=True
        )
        
        # Determine delivery methods based on severity
        send_sms = alert.severity in ['high', 'critical']
        
        # Send notifications
        count = UserService.bulk_create_notifications(
            users=list(users),
            notification_type='alert',
            title=alert.title,
            message=alert.message,
            priority=alert.severity,
            data={
                'alert_id': alert.id,
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'recommendations': alert.recommendations,
                'action_required': alert.action_required
            },
            send_push=True,
            send_sms=send_sms
        )
        
        # Update recipients count
        alert.recipients_count = count
        alert.save(update_fields=['recipients_count'])
        
        logger.info(f'Sent alert "{alert.title}" to {count} users')
        return count
    
    @staticmethod
    def check_weather_alerts():
        """
        Check for weather alerts from API and create system alerts
        
        Returns:
            int: Number of alerts created
        """
        from apps.weather.models import WeatherStation
        
        stations = WeatherStation.objects.filter(is_active=True)
        created_count = 0
        
        for station in stations:
            try:
                # Get weather alerts from API
                alerts = weather_api.get_weather_alerts(
                    float(station.latitude),
                    float(station.longitude)
                )
                
                for alert_data in alerts:
                    # Check if alert already exists
                    exists = Alert.objects.filter(
                        title=alert_data['event'],
                        counties__contains=[station.county],
                        start_time=alert_data['start']
                    ).exists()
                    
                    if not exists:
                        # Create new alert
                        Alert.objects.create(
                            alert_type='weather',
                            severity='high',
                            title=alert_data['event'],
                            message=alert_data['description'],
                            counties=[station.county],
                            start_time=alert_data['start'],
                            end_time=alert_data['end'],
                            status='active',
                            recommendations='Follow weather advisory guidelines.'
                        )
                        created_count += 1
                        
            except Exception as e:
                logger.error(f'Error checking weather alerts for {station.code}: {str(e)}')
        
        logger.info(f'Created {created_count} weather alerts')
        return created_count
    
    @staticmethod
    def get_alert_statistics() -> dict:
        """
        Get statistics about alerts
        
        Returns:
            dict: Alert statistics
        """
        from django.db.models import Count
        
        total = Alert.objects.count()
        by_type = Alert.objects.values('alert_type').annotate(count=Count('id'))
        by_severity = Alert.objects.values('severity').annotate(count=Count('id'))
        
        active_count = Alert.objects.filter(status='active').count()
        
        return {
            'total_alerts': total,
            'active_alerts': active_count,
            'by_type': list(by_type),
            'by_severity': list(by_severity),
        }
