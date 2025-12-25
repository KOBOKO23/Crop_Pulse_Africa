"""
Tests for Weather app
"""
from django.test import TestCase
from django.utils import timezone
from .models import WeatherStation, WeatherData, WeatherForecast, WeatherAdvisory
from apps.users.models import User


class WeatherStationTests(TestCase):
    def test_create_station(self):
        station = WeatherStation.objects.create(
            name='Nairobi Station',
            code='NRB001',
            latitude=-1.2921,
            longitude=36.8219,
            county='Nairobi',
            elevation=1795,
            is_active=True
        )
        
        self.assertEqual(station.name, 'Nairobi Station')
        self.assertEqual(station.code, 'NRB001')
        self.assertTrue(station.is_active)


class WeatherDataTests(TestCase):
    def test_create_weather_data(self):
        weather = WeatherData.objects.create(
            latitude=-1.2921,
            longitude=36.8219,
            county='Nairobi',
            temperature=25.5,
            humidity=65,
            pressure=1013,
            wind_speed=10.5,
            rainfall=0,
            condition='Clear',
            description='Clear sky',
            source='api',
            recorded_at=timezone.now()
        )
        
        self.assertEqual(weather.county, 'Nairobi')
        self.assertEqual(float(weather.temperature), 25.5)
        self.assertEqual(weather.condition, 'Clear')
