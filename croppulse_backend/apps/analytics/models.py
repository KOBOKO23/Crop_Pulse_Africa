"""
Analytics models for CropPulse Africa
"""
from django.db import models
from django.conf import settings


class DashboardMetric(models.Model):
    """Store computed dashboard metrics"""
    
    METRIC_TYPES = [
        ('users', 'User Metrics'),
        ('weather', 'Weather Metrics'),
        ('observations', 'Observation Metrics'),
        ('alerts', 'Alert Metrics'),
        ('community', 'Community Metrics'),
    ]
    
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    metric_name = models.CharField(max_length=100)
    metric_value = models.JSONField()
    
    # Optional filters
    county = models.CharField(max_length=100, blank=True)
    date_range_start = models.DateField(blank=True, null=True)
    date_range_end = models.DateField(blank=True, null=True)
    
    computed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard_metrics'
        verbose_name = 'Dashboard Metric'
        verbose_name_plural = 'Dashboard Metrics'
        ordering = ['-computed_at']
        indexes = [
            models.Index(fields=['metric_type', 'metric_name']),
            models.Index(fields=['county']),
        ]
    
    def __str__(self):
        return f"{self.metric_type} - {self.metric_name}"


class ActivityLog(models.Model):
    """Log user activities for analytics"""
    
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('observation', 'Observation Created'),
        ('alert_view', 'Alert Viewed'),
        ('forum_post', 'Forum Post Created'),
        ('message_sent', 'Message Sent'),
        ('weather_check', 'Weather Checked'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs'
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.activity_type} - {self.user.full_name if self.user else 'Anonymous'}"
