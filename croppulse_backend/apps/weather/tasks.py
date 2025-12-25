"""
Celery tasks for Weather app
"""
from celery import shared_task
from .services import WeatherService
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_weather_updates():
    """Fetch weather updates for all active stations"""
    try:
        count = WeatherService.update_weather_for_all_stations()
        logger.info(f'Updated weather for {count} stations')
        return count
    except Exception as e:
        logger.error(f'Error fetching weather updates: {str(e)}')
        return 0


@shared_task
def send_daily_summaries():
    """Send daily weather summaries to users"""
    from apps.users.models import User
    from apps.users.services import UserService
    
    # Get all farmers
    farmers = User.objects.filter(role='farmer', is_active=True)
    sent_count = 0
    
    for farmer in farmers:
        if farmer.county:
            try:
                summary = WeatherService.get_weather_summary(farmer.county, days=1)
                
                if summary:
                    message = (
                        f"Today's weather in {farmer.county}: "
                        f"Avg temp {summary['average_temperature']}°C, "
                        f"Humidity {summary['average_humidity']}%, "
                        f"Rainfall {summary['average_rainfall']}mm"
                    )
                    
                    UserService.create_notification(
                        user=farmer,
                        notification_type='advisory',
                        title='Daily Weather Summary',
                        message=message,
                        priority='low',
                        send_push=True,
                        send_sms=False
                    )
                    
                    sent_count += 1
                    
            except Exception as e:
                logger.error(f'Error sending summary to {farmer.id}: {str(e)}')
    
    logger.info(f'Sent daily summaries to {sent_count} farmers')
    return sent_count
