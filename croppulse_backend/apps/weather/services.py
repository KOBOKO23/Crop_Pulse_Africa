"""
Business logic services for Weather app
"""
from django.utils import timezone
from django.db.models import Q, Avg
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .models import WeatherData, WeatherForecast, WeatherAdvisory, WeatherStation
from services.weather_api import weather_api
from services.geocoding import geocoding_service
from apps.users.services import UserService
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """Service class for weather-related operations"""
    
    @staticmethod
    def fetch_current_weather(latitude: float, longitude: float) -> Dict:
        """
        Fetch current weather from API and optionally save to database
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            dict: Current weather data
        """
        try:
            # Fetch from API
            weather_data = weather_api.get_current_weather(latitude, longitude)
            
            # Get county from coordinates
            location = geocoding_service.reverse_geocode(latitude, longitude)
            county = location.get('county', '')
            
            # Save to database
            WeatherData.objects.create(
                latitude=latitude,
                longitude=longitude,
                county=county,
                temperature=weather_data['temperature'],
                feels_like=weather_data.get('feels_like'),
                temp_min=weather_data.get('temp_min'),
                temp_max=weather_data.get('temp_max'),
                humidity=weather_data['humidity'],
                pressure=weather_data['pressure'],
                wind_speed=weather_data['wind_speed'],
                wind_direction=weather_data.get('wind_direction'),
                rainfall=weather_data.get('rainfall', 0),
                clouds=weather_data.get('clouds'),
                visibility=weather_data.get('visibility'),
                condition=weather_data['condition'],
                description=weather_data['description'],
                icon=weather_data.get('icon', ''),
                source='api',
                recorded_at=weather_data['timestamp']
            )
            
            return weather_data
            
        except Exception as e:
            logger.error(f'Error fetching current weather: {str(e)}')
            raise
    
    @staticmethod
    def fetch_forecast(latitude: float, longitude: float, days: int = 7) -> List[Dict]:
        """
        Fetch weather forecast from API and save to database
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast
            
        Returns:
            list: Weather forecast data
        """
        try:
            # Fetch from API
            forecast_data = weather_api.get_forecast(latitude, longitude, days)
            
            # Get county
            location = geocoding_service.reverse_geocode(latitude, longitude)
            county = location.get('county', '')
            
            # Save forecasts to database
            for forecast in forecast_data:
                temp_avg = (forecast['temp_min'] + forecast['temp_max']) / 2
                
                WeatherForecast.objects.update_or_create(
                    latitude=latitude,
                    longitude=longitude,
                    forecast_date=forecast['date'],
                    defaults={
                        'county': county,
                        'temp_min': forecast['temp_min'],
                        'temp_max': forecast['temp_max'],
                        'temp_avg': temp_avg,
                        'humidity': forecast['humidity'],
                        'wind_speed': forecast['wind_speed'],
                        'rainfall': forecast['rainfall'],
                        'pop': forecast['pop'],
                        'condition': forecast['condition'],
                        'description': forecast['description'],
                        'icon': forecast.get('icon', ''),
                    }
                )
            
            return forecast_data
            
        except Exception as e:
            logger.error(f'Error fetching forecast: {str(e)}')
            raise
    
    @staticmethod
    def get_weather_summary(county: str, days: int = 7) -> Dict:
        """
        Get weather summary for a county
        
        Args:
            county: County name
            days: Number of days to analyze
            
        Returns:
            dict: Weather summary statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        weather_records = WeatherData.objects.filter(
            county__iexact=county,
            recorded_at__gte=start_date
        )
        
        if not weather_records.exists():
            return {}
        
        aggregates = weather_records.aggregate(
            avg_temp=Avg('temperature'),
            avg_humidity=Avg('humidity'),
            total_rainfall=Avg('rainfall'),
            avg_wind_speed=Avg('wind_speed')
        )
        
        return {
            'county': county,
            'period_days': days,
            'average_temperature': round(aggregates['avg_temp'] or 0, 2),
            'average_humidity': round(aggregates['avg_humidity'] or 0, 2),
            'average_rainfall': round(aggregates['total_rainfall'] or 0, 2),
            'average_wind_speed': round(aggregates['avg_wind_speed'] or 0, 2),
            'record_count': weather_records.count(),
        }
    
    @staticmethod
    def create_advisory(
        title: str,
        message: str,
        severity: str,
        counties: List[str],
        recommendations: str,
        valid_from: datetime,
        valid_until: datetime,
        created_by: User
    ) -> WeatherAdvisory:
        """
        Create a weather advisory
        
        Args:
            title: Advisory title
            message: Advisory message
            severity: Severity level
            counties: List of affected counties
            recommendations: Recommendations text
            valid_from: Start date
            valid_until: End date
            created_by: User creating the advisory
            
        Returns:
            WeatherAdvisory instance
        """
        advisory = WeatherAdvisory.objects.create(
            title=title,
            message=message,
            severity=severity,
            counties=counties,
            recommendations=recommendations,
            valid_from=valid_from,
            valid_until=valid_until,
            created_by=created_by
        )
        
        # Notify affected users
        WeatherService.notify_advisory(advisory)
        
        return advisory
    
    @staticmethod
    def notify_advisory(advisory: WeatherAdvisory):
        """
        Send notifications for a weather advisory
        
        Args:
            advisory: WeatherAdvisory instance
        """
        # Get users in affected counties
        users = User.objects.filter(
            county__in=advisory.counties,
            is_active=True
        )
        
        # Send notifications
        UserService.bulk_create_notifications(
            users=list(users),
            notification_type='advisory',
            title=advisory.title,
            message=advisory.message,
            priority='high' if advisory.severity in ['warning', 'emergency'] else 'medium',
            data={
                'advisory_id': advisory.id,
                'severity': advisory.severity,
                'recommendations': advisory.recommendations
            },
            send_push=True,
            send_sms=advisory.severity in ['warning', 'emergency']
        )
        
        logger.info(f'Sent advisory notifications to {users.count()} users')
    
    @staticmethod
    def get_active_advisories(county: Optional[str] = None) -> List[WeatherAdvisory]:
        """
        Get currently active advisories
        
        Args:
            county: Optional county filter
            
        Returns:
            list: Active WeatherAdvisory instances
        """
        now = timezone.now()
        
        query = Q(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )
        
        if county:
            query &= Q(counties__contains=[county])
        
        return list(WeatherAdvisory.objects.filter(query))
    
    @staticmethod
    def update_weather_for_all_stations():
        """
        Fetch and update weather data for all active stations
        
        Returns:
            int: Number of stations updated
        """
        stations = WeatherStation.objects.filter(is_active=True)
        updated_count = 0
        
        for station in stations:
            try:
                weather_data = weather_api.get_current_weather(
                    float(station.latitude),
                    float(station.longitude)
                )
                
                WeatherData.objects.create(
                    station=station,
                    latitude=station.latitude,
                    longitude=station.longitude,
                    county=station.county,
                    temperature=weather_data['temperature'],
                    feels_like=weather_data.get('feels_like'),
                    humidity=weather_data['humidity'],
                    pressure=weather_data['pressure'],
                    wind_speed=weather_data['wind_speed'],
                    wind_direction=weather_data.get('wind_direction'),
                    rainfall=weather_data.get('rainfall', 0),
                    condition=weather_data['condition'],
                    description=weather_data['description'],
                    source='station',
                    recorded_at=weather_data['timestamp']
                )
                
                updated_count += 1
                
            except Exception as e:
                logger.error(f'Error updating station {station.code}: {str(e)}')
        
        logger.info(f'Updated weather for {updated_count} stations')
        return updated_count
