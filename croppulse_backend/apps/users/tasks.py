"""
Celery tasks for Users app
"""
from celery import shared_task
from .services import UserService
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_notifications():
    """Clean up old read notifications"""
    deleted_count = UserService.cleanup_old_notifications(days=30)
    logger.info(f'Cleaned up {deleted_count} old notifications')
    return deleted_count


@shared_task
def send_bulk_notification(user_ids, notification_type, title, message, priority='medium', data=None):
    """Send notifications to multiple users"""
    from .models import User
    
    users = User.objects.filter(id__in=user_ids)
    count = UserService.bulk_create_notifications(
        users=users,
        notification_type=notification_type,
        title=title,
        message=message,
        priority=priority,
        data=data or {},
        send_push=True,
        send_sms=False
    )
    
    logger.info(f'Sent {count} notifications')
    return count
