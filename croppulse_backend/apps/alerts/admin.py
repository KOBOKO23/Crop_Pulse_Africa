"""
Admin configuration for Alerts app
"""
from django.contrib import admin
from .models import Alert, AlertAcknowledgment, AlertLog


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'severity', 'status', 'recipients_count', 'start_time', 'end_time', 'created_at']
    list_filter = ['alert_type', 'severity', 'status', 'created_at']
    search_fields = ['title', 'message']
    date_hierarchy = 'created_at'
    raw_id_fields = ['created_by']
    ordering = ['-created_at']


@admin.register(AlertAcknowledgment)
class AlertAcknowledgmentAdmin(admin.ModelAdmin):
    list_display = ['alert', 'user', 'acknowledged_at']
    list_filter = ['acknowledged_at']
    raw_id_fields = ['alert', 'user']
    date_hierarchy = 'acknowledged_at'
    ordering = ['-acknowledged_at']


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ['alert', 'user', 'delivery_method', 'was_successful', 'delivered_at']
    list_filter = ['delivery_method', 'was_successful', 'delivered_at']
    raw_id_fields = ['alert', 'user']
    date_hierarchy = 'delivered_at'
    ordering = ['-delivered_at']
