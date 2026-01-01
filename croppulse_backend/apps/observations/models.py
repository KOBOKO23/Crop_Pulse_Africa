"""
Observation models for CropPulse Africa
"""
from django.db import models
from django.conf import settings
from core.validators import validate_latitude, validate_longitude
from core.utils import get_upload_path

# Named functions for upload_to
def observation_image_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'observations')

def audio_observation_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'audio_observations')

def crop_report_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'crop_reports')

def pest_disease_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'pest_disease')


class FarmObservation(models.Model):
    """Field observations from farmers and field officers"""
    
    OBSERVATION_TYPES = [
        ('weather', 'Weather Condition'),
        ('crop_health', 'Crop Health'),
        ('pest_disease', 'Pest/Disease'),
        ('soil', 'Soil Condition'),
        ('general', 'General Observation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    # Observer
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='observations'
    )
    
    # Observation details
    observation_type = models.CharField(max_length=20, choices=OBSERVATION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
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
    location_description = models.CharField(max_length=255, blank=True)
    
    # Media attachments
    image1 = models.ImageField(
        upload_to=observation_image_upload_to,
        blank=True,
        null=True
    )
    image2 = models.ImageField(
        upload_to=observation_image_upload_to,
        blank=True,
        null=True
    )
    image3 = models.ImageField(
        upload_to=observation_image_upload_to,
        blank=True,
        null=True
    )
    audio_note = models.FileField(
        upload_to=audio_observation_upload_to,
        blank=True,
        null=True
    )
    
    # Weather data at time of observation
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    # Verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_observations'
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    verification_notes = models.TextField(blank=True)
    
    # Quality score (0-100)
    quality_score = models.IntegerField(default=0)
    
    # Metadata
    is_public = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farm_observations'
        verbose_name = 'Farm Observation'
        verbose_name_plural = 'Farm Observations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['county', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.full_name}"


class CropReport(models.Model):
    """Crop growth and development reports"""
    
    GROWTH_STAGES = [
        ('planting', 'Planting'),
        ('germination', 'Germination'),
        ('vegetative', 'Vegetative Growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting/Grain Filling'),
        ('maturity', 'Maturity'),
        ('harvest', 'Harvest'),
    ]
    
    HEALTH_STATUS = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crop_reports'
    )
    
    # Crop details
    crop_type = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    area_planted = models.DecimalField(max_digits=10, decimal_places=2, help_text='Area in hectares')
    
    # Growth information
    planting_date = models.DateField()
    current_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS)
    
    # Conditions
    notes = models.TextField(blank=True)
    challenges = models.TextField(blank=True, help_text='Any challenges faced')
    
    # Images
    crop_image = models.ImageField(
        upload_to=crop_report_upload_to,
        blank=True,
        null=True
    )
    
    # Expected harvest
    expected_harvest_date = models.DateField(blank=True, null=True)
    expected_yield = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Expected yield in kg/tons'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'crop_reports'
        verbose_name = 'Crop Report'
        verbose_name_plural = 'Crop Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.crop_type} - {self.current_stage} by {self.user.full_name}"


class PestDiseaseReport(models.Model):
    """Reports of pests and diseases"""
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pest_disease_reports'
    )
    
    # Pest/Disease details
    name = models.CharField(max_length=255, help_text='Name of pest or disease')
    pest_or_disease = models.CharField(
        max_length=10,
        choices=[('pest', 'Pest'), ('disease', 'Disease')]
    )
    affected_crop = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    
    # Description
    symptoms = models.TextField(help_text='Describe the symptoms observed')
    affected_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Affected area in hectares'
    )
    
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
    
    # Images
    image1 = models.ImageField(
        upload_to=pest_disease_upload_to,
        blank=True,
        null=True
    )
    image2 = models.ImageField(
        upload_to=pest_disease_upload_to,
        blank=True,
        null=True
    )
    
    # Response
    control_measures_taken = models.TextField(blank=True)
    requires_assistance = models.BooleanField(default=False)
    
    # Status
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pest_disease_reports'
        verbose_name = 'Pest/Disease Report'
        verbose_name_plural = 'Pest/Disease Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['county', '-created_at']),
            models.Index(fields=['severity', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} on {self.affected_crop}"
