"""
Utility functions for CropPulse Africa
"""
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from django.utils import timezone
from django.core.cache import cache
import math


def generate_unique_id(prefix: str = '') -> str:
    """Generate a unique identifier with optional prefix"""
    unique_id = uuid.uuid4().hex[:12]
    return f"{prefix}{unique_id}" if prefix else unique_id


def generate_verification_code(length: int = 6) -> str:
    """Generate a numeric verification code"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])


def hash_value(value: str, salt: str = '') -> str:
    """Create SHA256 hash of a value with optional salt"""
    combined = f"{value}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def is_within_radius(
    center_lat: float, 
    center_lon: float, 
    point_lat: float, 
    point_lon: float, 
    radius_km: float
) -> bool:
    """Check if a point is within a given radius of a center point"""
    distance = calculate_distance(center_lat, center_lon, point_lat, point_lon)
    return distance <= radius_km


def get_kenyan_season(date: Optional[datetime] = None) -> str:
    """
    Determine the agricultural season in Kenya based on the date
    Kenya has two main rainy seasons:
    - Long rains: March to May
    - Short rains: October to December
    """
    if date is None:
        date = timezone.now()
    
    month = date.month
    
    if 3 <= month <= 5:
        return 'long_rains'
    elif 10 <= month <= 12:
        return 'short_rains'
    elif 6 <= month <= 9:
        return 'dry_season_1'
    else:  # January, February
        return 'dry_season_2'


def format_phone_number(phone: str) -> str:
    """
    Standardize phone number format to international format (+254XXXXXXXXX)
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Convert to international format
    if digits.startswith('254'):
        return f'+{digits}'
    elif digits.startswith('0'):
        return f'+254{digits[1:]}'
    elif len(digits) == 9:
        return f'+254{digits}'
    else:
        return phone  # Return original if can't parse


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments"""
    key_parts = [prefix] + [str(arg) for arg in args]
    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        key_parts.extend([f"{k}:{v}" for k, v in sorted_kwargs])
    return ':'.join(key_parts)


def get_or_set_cache(key: str, callable_func, timeout: int = 300):
    """Get value from cache or set it using the callable function"""
    value = cache.get(key)
    if value is None:
        value = callable_func()
        cache.set(key, value, timeout)
    return value


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to specified length with suffix"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_date_range(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Tuple[datetime, datetime]:
    """
    Parse date range strings and return datetime objects
    Defaults to last 30 days if not provided
    """
    if end_date:
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    else:
        end = timezone.now()
    
    if start_date:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    else:
        start = end - timedelta(days=30)
    
    return start, end


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove potentially dangerous characters"""
    # Keep only alphanumeric, dots, hyphens, and underscores
    sanitized = ''.join(c for c in filename if c.isalnum() or c in '.-_')
    # Ensure it doesn't start with a dot
    if sanitized.startswith('.'):
        sanitized = sanitized[1:]
    return sanitized or 'unnamed'


def get_upload_path(instance, filename: str, folder: str = 'uploads') -> str:
    """
    Generate upload path for files
    Format: folder/YYYY/MM/DD/unique_id_filename
    """
    now = timezone.now()
    sanitized = sanitize_filename(filename)
    unique_id = uuid.uuid4().hex[:8]
    
    return f"{folder}/{now.year}/{now.month:02d}/{now.day:02d}/{unique_id}_{sanitized}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    return ((new_value - old_value) / old_value) * 100


def get_county_from_coordinates(latitude: float, longitude: float) -> Optional[str]:
    """
    Approximate county from coordinates (simplified version)
    In production, this should use a proper geocoding service
    """
    # This is a simplified placeholder
    # In production, integrate with services/geocoding.py
    COUNTY_BOUNDS = {
        'Nairobi': {'lat': (-1.44, -1.16), 'lon': (36.65, 37.10)},
        'Mombasa': {'lat': (-4.15, -3.95), 'lon': (39.55, 39.75)},
        'Kisumu': {'lat': (-0.20, 0.20), 'lon': (34.60, 35.00)},
        # Add more counties as needed
    }
    
    for county, bounds in COUNTY_BOUNDS.items():
        if (bounds['lat'][0] <= latitude <= bounds['lat'][1] and
            bounds['lon'][0] <= longitude <= bounds['lon'][1]):
            return county
    
    return None


def get_weather_icon(condition: str) -> str:
    """Map weather condition to icon name"""
    condition_lower = condition.lower()
    
    if 'rain' in condition_lower or 'shower' in condition_lower:
        return 'rain'
    elif 'thunder' in condition_lower or 'storm' in condition_lower:
        return 'thunderstorm'
    elif 'cloud' in condition_lower:
        return 'cloudy'
    elif 'clear' in condition_lower or 'sunny' in condition_lower:
        return 'sunny'
    elif 'fog' in condition_lower or 'mist' in condition_lower:
        return 'foggy'
    elif 'wind' in condition_lower:
        return 'windy'
    else:
        return 'default'


def validate_coordinates_in_kenya(latitude: float, longitude: float) -> bool:
    """Validate that coordinates are within Kenya's approximate bounds"""
    return (-5.0 <= latitude <= 5.5) and (33.5 <= longitude <= 42.0)
