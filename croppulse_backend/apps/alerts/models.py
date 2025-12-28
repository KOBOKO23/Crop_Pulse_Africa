"""
Alert models for CropPulse Africa
"""
from django.db import models
from django.conf import settings


class Alert(models.Model):
    """System-wide alerts for weather, agricultural advisories, etc."""
    
    ALERT_TYPES = [
        ('weather', 'Weather Alert'),
        ('drought', 'Drought Warning'),
        ('flood', 'Flood Warning'),
        ('pest', 'Pest Outbreak'),
        ('disease', 'Disease Outbreak'),
        ('advisory', 'Agricultural Advisory'),
        ('system', 'System Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Information'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Alert details
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=255)
    message = models.TextField()
    description = models.TextField(blank=True, help_text='Detailed description')
    
    # Target area
    counties = models.JSONField(default=list, help_text='Affected counties')
    subcounties = models.JSONField(default=list, blank=True, help_text='Affected subcounties')
    
    # Validity period
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Recommendations
    recommendations = models.TextField(blank=True)
    action_required = models.BooleanField(default=False)
    action_description = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_alerts'
    )
    recipients_count = models.IntegerField(default=0)
    
    # Acknowledgment tracking
    require_acknowledgment = models.BooleanField(default=False)
    acknowledgment_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alerts'
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['alert_type', '-created_at']),
            models.Index(fields=['start_time', 'end_time']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.severity})"


class AlertAcknowledgment(models.Model):
    """Track user acknowledgments of alerts"""
    
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='acknowledgments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    acknowledged_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'alert_acknowledgments'
        verbose_name = 'Alert Acknowledgment'
        verbose_name_plural = 'Alert Acknowledgments'
        unique_together = [['alert', 'user']]
        ordering = ['-acknowledged_at']
    
    def __str__(self):
        return f"{self.user.full_name} acknowledged {self.alert.title}"


class AlertLog(models.Model):
    """Log of alert delivery to users"""
    
    DELIVERY_METHODS = [
        ('push', 'Push Notification'),
        ('sms', 'SMS'),
        ('email', 'Email'),
    ]
    
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='delivery_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS)
    delivered_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        db_table = 'alert_logs'
        verbose_name = 'Alert Log'
        verbose_name_plural = 'Alert Logs'
        ordering = ['-delivered_at']
        indexes = [
            models.Index(fields=['alert', 'user']),
        ]
    
    def __str__(self):
        return f"{self.alert.title} to {self.user.full_name} via {self.delivery_method}"
