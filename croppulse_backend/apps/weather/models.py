"""
Weather models for CropPulse Africa
"""
from django.db import models
from django.conf import settings
from core.validators import (
    validate_latitude, validate_longitude,
    validate_temperature, validate_rainfall,
    validate_humidity, validate_wind_speed
)


class WeatherStation(models.Model):
    """Weather monitoring stations"""
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude]
    )
    
    county = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100, blank=True)
    elevation = models.IntegerField(help_text='Elevation in meters')
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'weather_stations'
        verbose_name = 'Weather Station'
        verbose_name_plural = 'Weather Stations'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class WeatherData(models.Model):
    """Current and historical weather data"""
    
    SOURCE_CHOICES = [
        ('api', 'API'),
        ('station', 'Weather Station'),
        ('observation', 'User Observation'),
    ]
    
    station = models.ForeignKey(
        WeatherStation,
        on_delete=models.CASCADE,
        related_name='weather_data',
        null=True,
        blank=True
    )
    
    # Location (for API data without station)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude],
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude],
        null=True,
        blank=True
    )
    county = models.CharField(max_length=100, blank=True)
    
    # Weather measurements
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[validate_temperature],
        help_text='Temperature in Celsius'
    )
    feels_like = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    temp_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    temp_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    humidity = models.IntegerField(
        validators=[validate_humidity],
        help_text='Humidity percentage'
    )
    pressure = models.IntegerField(help_text='Atmospheric pressure in hPa')
    
    wind_speed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[validate_wind_speed],
        help_text='Wind speed in km/h'
    )
    wind_direction = models.IntegerField(
        help_text='Wind direction in degrees',
        blank=True,
        null=True
    )
    
    rainfall = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[validate_rainfall],
        default=0,
        help_text='Rainfall in mm'
    )
    
    clouds = models.IntegerField(
        help_text='Cloud coverage percentage',
        blank=True,
        null=True
    )
    visibility = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Visibility in km',
        blank=True,
        null=True
    )
    
    # Weather condition
    condition = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10, blank=True)
    
    # Metadata
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='api')
    recorded_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'weather_data'
        verbose_name = 'Weather Data'
        verbose_name_plural = 'Weather Data'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['county', '-recorded_at']),
            models.Index(fields=['latitude', 'longitude', '-recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.condition} at {self.recorded_at}"


class WeatherForecast(models.Model):
    """Weather forecast data"""
    
    # Location
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude]
    )
    county = models.CharField(max_length=100)
    
    # Forecast date
    forecast_date = models.DateField()
    
    # Temperature
    temp_min = models.DecimalField(max_digits=5, decimal_places=2)
    temp_max = models.DecimalField(max_digits=5, decimal_places=2)
    temp_avg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # Other conditions
    humidity = models.IntegerField(validators=[validate_humidity])
    wind_speed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[validate_wind_speed]
    )
    rainfall = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[validate_rainfall],
        default=0
    )
    
    # Probability of precipitation
    pop = models.IntegerField(help_text='Probability of precipitation (%)')
    
    # Weather condition
    condition = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'weather_forecasts'
        verbose_name = 'Weather Forecast'
        verbose_name_plural = 'Weather Forecasts'
        ordering = ['forecast_date']
        unique_together = [['latitude', 'longitude', 'forecast_date']]
        indexes = [
            models.Index(fields=['county', 'forecast_date']),
            models.Index(fields=['forecast_date']),
        ]
    
    def __str__(self):
        return f"Forecast for {self.forecast_date} - {self.county}"


class WeatherAdvisory(models.Model):
    """Weather-based agricultural advisories"""
    
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('watch', 'Watch'),
        ('warning', 'Warning'),
        ('emergency', 'Emergency'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    # Target area
    counties = models.JSONField(default=list)
    
    # Recommendations
    recommendations = models.TextField()
    
    # Validity period
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    
    # Author
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_advisories'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'weather_advisories'
        verbose_name = 'Weather Advisory'
        verbose_name_plural = 'Weather Advisories'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.severity})"
