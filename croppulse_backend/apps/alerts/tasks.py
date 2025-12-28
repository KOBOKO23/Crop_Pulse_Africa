"""
Celery tasks for Alerts app
"""
from celery import shared_task
from .services import AlertService
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_weather_alerts():
    """Check for weather alerts from external API"""
    try:
        count = AlertService.check_weather_alerts()
        logger.info(f'Checked weather alerts, created {count} new alerts')
        return count
    except Exception as e:
        logger.error(f'Error checking weather alerts: {str(e)}')
        return 0
