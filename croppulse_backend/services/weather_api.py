"""
Weather API Service for CropPulse Africa
Integrates with OpenWeatherMap API
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from core.exceptions import WeatherServiceError
from core.utils import cache_key
import logging

logger = logging.getLogger(__name__)


class WeatherAPIService:
    """Service for fetching weather data from OpenWeatherMap"""
    
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        if not self.api_key:
            logger.warning('OpenWeatherMap API key not configured')
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Get current weather for coordinates
        Returns: Weather data dictionary
        """
        cache_key_str = cache_key('weather:current', latitude, longitude)
        cached_data = cache.get(cache_key_str)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.BASE_URL}/weather'
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather_data = self._parse_current_weather(data)
            
            # Cache for 30 minutes
            cache.set(cache_key_str, weather_data, 1800)
            
            return weather_data
            
        except requests.RequestException as e:
            logger.error(f'Weather API error: {str(e)}')
            raise WeatherServiceError(f'Failed to fetch weather data: {str(e)}')
    
    def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> List[Dict]:
        """
        Get weather forecast for coordinates
        Returns: List of daily forecast dictionaries
        """
        cache_key_str = cache_key('weather:forecast', latitude, longitude, days)
        cached_data = cache.get(cache_key_str)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.BASE_URL}/forecast'
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8,  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast_data = self._parse_forecast(data, days)
            
            # Cache for 1 hour
            cache.set(cache_key_str, forecast_data, 3600)
            
            return forecast_data
            
        except requests.RequestException as e:
            logger.error(f'Forecast API error: {str(e)}')
            raise WeatherServiceError(f'Failed to fetch forecast data: {str(e)}')
    
    def get_historical_weather(
        self, 
        latitude: float, 
        longitude: float, 
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Get historical weather data
        Note: Requires paid OpenWeatherMap subscription
        """
        try:
            historical_data = []
            current_date = start_date
            
            while current_date <= end_date:
                timestamp = int(current_date.timestamp())
                url = f'{self.BASE_URL}/onecall/timemachine'
                params = {
                    'lat': latitude,
                    'lon': longitude,
                    'dt': timestamp,
                    'appid': self.api_key,
                    'units': 'metric',
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                historical_data.append(self._parse_historical_data(data))
                current_date += timedelta(days=1)
            
            return historical_data
            
        except requests.RequestException as e:
            logger.error(f'Historical weather API error: {str(e)}')
            raise WeatherServiceError(f'Failed to fetch historical data: {str(e)}')
    
    def _parse_current_weather(self, data: Dict) -> Dict:
        """Parse current weather API response"""
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'rainfall': data.get('rain', {}).get('1h', 0),
            'timestamp': datetime.fromtimestamp(data['dt']),
        }
    
    def _parse_forecast(self, data: Dict, days: int) -> List[Dict]:
        """Parse forecast API response into daily summaries"""
        daily_forecasts = {}
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.date()
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    'date': date_key,
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'rainfall': item.get('rain', {}).get('3h', 0),
                    'pop': item.get('pop', 0) * 100,  # Probability of precipitation
                }
            else:
                # Update min/max temperatures
                daily_forecasts[date_key]['temp_min'] = min(
                    daily_forecasts[date_key]['temp_min'],
                    item['main']['temp_min']
                )
                daily_forecasts[date_key]['temp_max'] = max(
                    daily_forecasts[date_key]['temp_max'],
                    item['main']['temp_max']
                )
                # Accumulate rainfall
                daily_forecasts[date_key]['rainfall'] += item.get('rain', {}).get('3h', 0)
        
        return list(daily_forecasts.values())[:days]
    
    def _parse_historical_data(self, data: Dict) -> Dict:
        """Parse historical weather data"""
        current = data['current']
        return {
            'timestamp': datetime.fromtimestamp(current['dt']),
            'temperature': current['temp'],
            'humidity': current['humidity'],
            'pressure': current['pressure'],
            'wind_speed': current['wind_speed'],
            'clouds': current['clouds'],
            'condition': current['weather'][0]['main'],
            'description': current['weather'][0]['description'],
        }
    
    def get_weather_alerts(self, latitude: float, longitude: float) -> List[Dict]:
        """Get weather alerts for a location"""
        try:
            url = f'{self.BASE_URL}/onecall'
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'exclude': 'current,minutely,hourly,daily',
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            alerts = data.get('alerts', [])
            return [
                {
                    'event': alert['event'],
                    'start': datetime.fromtimestamp(alert['start']),
                    'end': datetime.fromtimestamp(alert['end']),
                    'description': alert['description'],
                    'sender': alert.get('sender_name', 'Unknown'),
                }
                for alert in alerts
            ]
            
        except requests.RequestException as e:
            logger.error(f'Weather alerts API error: {str(e)}')
            return []


# Singleton instance
weather_api = WeatherAPIService()
