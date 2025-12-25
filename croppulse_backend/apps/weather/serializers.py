"""
Serializers for Weather app
"""
from rest_framework import serializers
from .models import WeatherStation, WeatherData, WeatherForecast, WeatherAdvisory


class WeatherStationSerializer(serializers.ModelSerializer):
    """Serializer for weather stations"""
    
    class Meta:
        model = WeatherStation
        fields = [
            'id', 'name', 'code', 'latitude', 'longitude',
            'county', 'subcounty', 'elevation', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer for weather data"""
    
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'station', 'station_name', 'latitude', 'longitude', 'county',
            'temperature', 'feels_like', 'temp_min', 'temp_max',
            'humidity', 'pressure', 'wind_speed', 'wind_direction',
            'rainfall', 'clouds', 'visibility', 'condition', 'description',
            'icon', 'source', 'recorded_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WeatherDataSimpleSerializer(serializers.ModelSerializer):
    """Simplified serializer for weather data"""
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'temperature', 'humidity', 'rainfall', 'wind_speed',
            'condition', 'description', 'icon', 'recorded_at'
        ]


class WeatherForecastSerializer(serializers.ModelSerializer):
    """Serializer for weather forecast"""
    
    class Meta:
        model = WeatherForecast
        fields = [
            'id', 'latitude', 'longitude', 'county', 'forecast_date',
            'temp_min', 'temp_max', 'temp_avg', 'humidity', 'wind_speed',
            'rainfall', 'pop', 'condition', 'description', 'icon',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeatherAdvisorySerializer(serializers.ModelSerializer):
    """Serializer for weather advisory"""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = WeatherAdvisory
        fields = [
            'id', 'title', 'message', 'severity', 'counties',
            'recommendations', 'valid_from', 'valid_until', 'is_active',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class CurrentWeatherRequestSerializer(serializers.Serializer):
    """Serializer for current weather request"""
    
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)


class ForecastRequestSerializer(serializers.Serializer):
    """Serializer for forecast request"""
    
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    days = serializers.IntegerField(default=7, min_value=1, max_value=14)
