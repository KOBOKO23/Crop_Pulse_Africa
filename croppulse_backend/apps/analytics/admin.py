"""
Admin configuration for Analytics app
"""
from django.contrib import admin
from .models import DashboardMetric, ActivityLog


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'metric_name', 'county', 'computed_at']
    list_filter = ['metric_type', 'county', 'computed_at']
    search_fields = ['metric_name', 'county']
    date_hierarchy = 'computed_at'
    ordering = ['-computed_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__full_name', 'description']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
