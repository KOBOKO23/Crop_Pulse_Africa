"""
Admin configuration for Weather app
"""
from django.contrib import admin
from .models import WeatherStation, WeatherData, WeatherForecast, WeatherAdvisory


@admin.register(WeatherStation)
class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'county', 'latitude', 'longitude', 'is_active', 'created_at']
    list_filter = ['is_active', 'county', 'created_at']
    search_fields = ['name', 'code', 'county']
    ordering = ['name']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['recorded_at', 'county', 'temperature', 'humidity', 'rainfall', 'condition', 'source']
    list_filter = ['source', 'condition', 'county', 'recorded_at']
    search_fields = ['county', 'condition']
    date_hierarchy = 'recorded_at'
    ordering = ['-recorded_at']


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ['forecast_date', 'county', 'temp_min', 'temp_max', 'rainfall', 'condition']
    list_filter = ['condition', 'county', 'forecast_date']
    search_fields = ['county', 'condition']
    date_hierarchy = 'forecast_date'
    ordering = ['forecast_date']


@admin.register(WeatherAdvisory)
class WeatherAdvisoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'valid_from', 'valid_until', 'is_active', 'created_by', 'created_at']
    list_filter = ['severity', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    date_hierarchy = 'created_at'
    raw_id_fields = ['created_by']
    ordering = ['-created_at']
