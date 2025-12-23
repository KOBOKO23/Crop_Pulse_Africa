"""
Celery configuration for CropPulse Africa
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'croppulse.settings.development')

app = Celery('croppulse')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Fetch weather updates every hour
    'fetch-weather-updates': {
        'task': 'apps.weather.tasks.fetch_weather_updates',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Check for weather alerts every 30 minutes
    'check-weather-alerts': {
        'task': 'apps.alerts.tasks.check_weather_alerts',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    # Send daily weather summaries at 6 AM
    'send-daily-weather-summaries': {
        'task': 'apps.weather.tasks.send_daily_summaries',
        'schedule': crontab(hour=6, minute=0),  # 6:00 AM daily
    },
    # Clean up old notifications weekly
    'cleanup-old-notifications': {
        'task': 'apps.users.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # 2:00 AM on Sundays
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
