"""
User models for CropPulse Africa
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core.validators import validate_latitude, validate_longitude
from core.utils import get_upload_path


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular user"""
        if not phone_number:
            raise ValueError(_('Phone number is required'))
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'hq_analyst')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """Custom User model for CropPulse Africa"""
    
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('field_officer', 'Field Officer'),
        ('hq_analyst', 'HQ Analyst'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('sw', 'Swahili'),
        ('ki', 'Kikuyu'),
        ('lu', 'Luhya'),
        ('ka', 'Kamba'),
    ]
    
    # Remove username, use phone number as primary identifier
    username = None
    
    # Core fields
    phone_number = PhoneNumberField(unique=True, region='KE')
    email = models.EmailField(_('email address'), blank=True, null=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Profile fields
    profile_picture = models.ImageField(
        upload_to=lambda instance, filename: get_upload_path(instance, filename, 'profile_pictures'),
        blank=True,
        null=True
    )
    county = models.CharField(max_length=100, blank=True)
    subcounty = models.CharField(max_length=100, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    verification_code_created_at = models.DateTimeField(blank=True, null=True)
    
    # Preferences
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    receive_sms_notifications = models.BooleanField(default=True)
    receive_push_notifications = models.BooleanField(default=True)
    
    # Device tokens for push notifications
    fcm_token = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'role']
    
    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
    
    @property
    def is_farmer(self):
        return self.role == 'farmer'
    
    @property
    def is_field_officer(self):
        return self.role == 'field_officer'
    
    @property
    def is_hq_analyst(self):
        return self.role == 'hq_analyst'


class FarmerProfile(models.Model):
    """Extended profile for farmers"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    
    # Farm details
    farm_name = models.CharField(max_length=255, blank=True)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text='Size in hectares')
    primary_crop = models.CharField(max_length=100)
    secondary_crops = models.JSONField(default=list, blank=True)
    
    # Location
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[validate_latitude],
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[validate_longitude],
        blank=True,
        null=True
    )
    
    # Farming experience
    years_of_experience = models.IntegerField(default=0)
    farming_type = models.CharField(
        max_length=50,
        choices=[
            ('subsistence', 'Subsistence'),
            ('commercial', 'Commercial'),
            ('mixed', 'Mixed'),
        ],
        default='subsistence'
    )
    
    # Additional info
    has_irrigation = models.BooleanField(default=False)
    has_greenhouse = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farmer_profiles'
        verbose_name = _('farmer profile')
        verbose_name_plural = _('farmer profiles')
    
    def __str__(self):
        return f"{self.user.full_name}'s Farm"


class FieldOfficerProfile(models.Model):
    """Extended profile for field officers"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='field_officer_profile')
    
    # Work details
    employee_id = models.CharField(max_length=50, unique=True)
    assigned_counties = models.JSONField(default=list)
    assigned_subcounties = models.JSONField(default=list)
    
    # Supervisor
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_officers'
    )
    
    # Work area
    coverage_area_radius = models.IntegerField(default=50, help_text='Radius in kilometers')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'field_officer_profiles'
        verbose_name = _('field officer profile')
        verbose_name_plural = _('field officer profiles')
    
    def __str__(self):
        return f"{self.user.full_name} - {self.employee_id}"


class Notification(models.Model):
    """User notifications"""
    
    TYPE_CHOICES = [
        ('alert', 'Weather Alert'),
        ('advisory', 'Advisory'),
        ('message', 'Message'),
        ('system', 'System'),
        ('community', 'Community'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    # For linking to related objects
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.IntegerField(blank=True, null=True)
    
    sent_via_push = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.full_name}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
