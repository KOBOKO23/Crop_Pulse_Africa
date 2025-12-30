"""
Geocoding Service for CropPulse Africa
Provides location-based utilities and reverse geocoding
"""
import requests
from typing import Dict, Optional, Tuple
from django.core.cache import cache
from core.exceptions import GeocodingServiceError
from core.utils import cache_key
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for geocoding and reverse geocoding operations"""
    
    # OpenStreetMap Nominatim API (free, but rate-limited)
    NOMINATIM_URL = 'https://nominatim.openstreetmap.org'
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'CropPulse-Africa/1.0 (contact@croppulse.africa)'
        }
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Dict:
        """
        Convert coordinates to address/location information
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            dict: Location information including county, subcounty, etc.
        """
        cache_key_str = cache_key('geocode:reverse', latitude, longitude)
        cached_data = cache.get(cache_key_str)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.NOMINATIM_URL}/reverse'
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1,
            }
            
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            location_data = self._parse_reverse_geocode(data)
            
            # Cache for 24 hours (locations don't change)
            cache.set(cache_key_str, location_data, 86400)
            
            return location_data
            
        except requests.RequestException as e:
            logger.error(f'Geocoding API error: {str(e)}')
            raise GeocodingServiceError(f'Failed to reverse geocode: {str(e)}')
    
    def geocode_address(self, address: str, country: str = 'Kenya') -> Optional[Tuple[float, float]]:
        """
        Convert address to coordinates
        
        Args:
            address: Address string
            country: Country name (default: Kenya)
            
        Returns:
            tuple: (latitude, longitude) or None if not found
        """
        cache_key_str = cache_key('geocode:forward', address, country)
        cached_data = cache.get(cache_key_str)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.NOMINATIM_URL}/search'
            params = {
                'q': f'{address}, {country}',
                'format': 'json',
                'limit': 1,
            }
            
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                result = (float(data[0]['lat']), float(data[0]['lon']))
                # Cache for 24 hours
                cache.set(cache_key_str, result, 86400)
                return result
            
            return None
            
        except requests.RequestException as e:
            logger.error(f'Geocoding API error: {str(e)}')
            return None
    
    def _parse_reverse_geocode(self, data: Dict) -> Dict:
        """Parse reverse geocoding API response"""
        address = data.get('address', {})
        
        return {
            'county': self._extract_county(address),
            'subcounty': address.get('county', ''),
            'ward': address.get('suburb', ''),
            'village': address.get('village', ''),
            'display_name': data.get('display_name', ''),
            'latitude': float(data.get('lat', 0)),
            'longitude': float(data.get('lon', 0)),
        }
    
    def _extract_county(self, address: Dict) -> str:
        """
        Extract Kenyan county from address components
        Kenyan administrative structure: County > Subcounty > Ward > Village
        """
        # Try different fields that might contain the county
        for field in ['state', 'region', 'county', 'province']:
            if field in address:
                county_name = address[field]
                # Clean up the name
                if 'County' in county_name:
                    return county_name.replace(' County', '')
                return county_name
        
        return ''
    
    def get_county_bounds(self, county_name: str) -> Optional[Dict]:
        """
        Get bounding box coordinates for a Kenyan county
        
        Args:
            county_name: Name of the county
            
        Returns:
            dict: Bounding box with min/max lat/lon
        """
        cache_key_str = cache_key('geocode:county_bounds', county_name)
        cached_data = cache.get(cache_key_str)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.NOMINATIM_URL}/search'
            params = {
                'q': f'{county_name} County, Kenya',
                'format': 'json',
                'limit': 1,
            }
            
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                bbox = data[0].get('boundingbox', [])
                if len(bbox) == 4:
                    bounds = {
                        'min_lat': float(bbox[0]),
                        'max_lat': float(bbox[1]),
                        'min_lon': float(bbox[2]),
                        'max_lon': float(bbox[3]),
                    }
                    # Cache for 7 days
                    cache.set(cache_key_str, bounds, 604800)
                    return bounds
            
            return None
            
        except requests.RequestException as e:
            logger.error(f'County bounds API error: {str(e)}')
            return None
    
    def get_nearest_town(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Get the nearest town/city to coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            str: Town/city name or None
        """
        location_data = self.reverse_geocode(latitude, longitude)
        return location_data.get('subcounty') or location_data.get('village')
    
    def validate_kenya_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        Validate that coordinates are within Kenya
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            bool: True if within Kenya bounds
        """
        # Kenya's approximate bounding box
        KENYA_BOUNDS = {
            'min_lat': -5.0,
            'max_lat': 5.5,
            'min_lon': 33.5,
            'max_lon': 42.0,
        }
        
        return (
            KENYA_BOUNDS['min_lat'] <= latitude <= KENYA_BOUNDS['max_lat'] and
            KENYA_BOUNDS['min_lon'] <= longitude <= KENYA_BOUNDS['max_lon']
        )


# Singleton instance
geocoding_service = GeocodingService()
