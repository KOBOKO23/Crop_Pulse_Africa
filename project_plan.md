# CropPulse Africa - Full Stack Development Plan
**Django + React Agricultural Meteorological Platform**

---

## 📋 Table of Contents
1. [Project Idea](#project-idea)
2. [Core Features](#core-features)
3. [Technology Stack](#technology-stack)
4. [Database Models](#database-models)
5. [API Endpoints](#api-endpoints)
6. [External APIs](#external-apis)
7. [5-Week Development Plan](#5-week-development-plan)
8. [Project Structure](#project-structure)
9. [Security & Authentication](#security--authentication)
10. [Deployment Strategy](#deployment-strategy)

---

## 🌾 Project Idea

**CropPulse Africa** is an agricultural meteorological intelligence platform designed for Kenya that bridges the gap between weather data and agricultural decision-making. The platform serves three distinct user roles:

### Target Users
1. **Farmers** (Primary) - Smallholder farmers who need:
   - Real-time weather updates
   - Crop health monitoring guidance
   - Direct communication with agricultural extension officers
   - Agricultural advisories and alerts

2. **Field Officers** (Secondary) - Agricultural extension officers who need:
   - Farmer report management system
   - Weather station monitoring tools
   - Field data collection forms
   - Area-wide performance analytics

3. **HQ Analysts** (Tertiary) - Ministry/department officials who need:
   - National/regional overview dashboards
   - Alert broadcasting system
   - System health monitoring
   - Data analytics and reporting

### Problem Statement
Kenyan smallholder farmers face significant crop losses due to:
- Lack of timely, accurate weather information
- Poor communication with agricultural extension services
- Limited access to agricultural expertise
- Delayed response to pest/disease outbreaks
- Inadequate early warning systems

### Solution
A web-based platform that provides:
- Localized weather forecasts from actual weather stations
- Easy-to-use observation reporting system (low literacy friendly)
- Direct farmer-to-officer communication
- SMS/App-based alert system
- Community knowledge sharing
- Data-driven decision support

---

## ⚡ Core Features

### 1. User Authentication & Management
- **Multi-role registration** (Farmer, Field Officer, HQ)
- **JWT-based authentication**
- **Role-based access control (RBAC)**
- **User profiles** with farm/area details
- **Password reset via SMS/Email**
- **User activity logging**

### 2. Farmer Portal Features
- **Personalized Dashboard**
  - Weather snapshot (current + 4-day forecast)
  - Crop health indicators
  - Days to harvest countdown
  - Active alerts counter

- **Observation Reporting System**
  - 3-step wizard form
  - 15+ visual observation options (icon-based for low literacy)
  - Severity rating (Mild, Moderate, Severe, Critical)
  - Photo uploads (up to 5 images)
  - Voice note recording
  - GPS auto-location

- **Weather Information**
  - Current conditions (temp, humidity, rainfall, wind)
  - 4-7 day forecast
  - Soil moisture indicators
  - Hourly predictions
  - Audio playback option (text-to-speech)

- **Alert System**
  - Push notifications
  - SMS alerts
  - Priority-based (Critical, High, Medium, Low)
  - Weather warnings
  - Pest/disease alerts
  - Agricultural advisories

- **Officer Communication**
  - Direct call functionality
  - In-app messaging
  - Officer availability status
  - Response tracking

- **Reports History**
  - View past submissions
  - Track status (Pending, In Progress, Resolved)
  - View officer responses
  - Download report PDFs

### 3. Field Officer Portal Features
- **Farmer Management Dashboard**
  - Active farmers list (127+ farmers per officer)
  - Pending reports queue (8 urgent, others prioritized)
  - Quick stats (reports today, response rate, etc.)

- **Report Review System**
  - Filterable report list (All, Pending, Urgent)
  - Detailed report view with photos/audio
  - Response form with rich text editor
  - Recommended actions checklist
  - Schedule site visits
  - Mark as resolved

- **Weather Station Monitoring**
  - Station status cards (Online, Warning, Offline)
  - Real-time readings display
  - Last update timestamps
  - Alert if station offline >30 mins
  - Historical data access

- **Field Data Collection**
  - Weather data entry form
  - Crop condition assessments
  - Pest activity logging
  - Photo documentation
  - GPS coordinates

- **Area Analytics**
  - Response rate metrics
  - Farmer engagement stats
  - Common issues tracker
  - Weekly/monthly reports
  - Performance trends

### 4. HQ Analytics Center Features
- **National Dashboard**
  - System-wide statistics (4,234 farmers, 47 officers, 31 stations)
  - Regional performance table (sortable, filterable)
  - System health monitoring (API, Database, Network)
  - Activity feed (real-time updates)

- **Alert Broadcasting System**
  - Create alert templates
  - Multi-channel delivery (App, SMS, Radio, Email)
  - Geographic targeting (county/sub-county level)
  - Crop-specific alerts
  - Schedule broadcast
  - Delivery status tracking
  - Engagement analytics

- **Weather Trends Visualization**
  - 7/14/30-day rainfall charts
  - Temperature patterns
  - Regional comparisons
  - Export data (CSV, Excel)

- **Station Network Management**
  - Station status overview (30 online, 1 maintenance)
  - Uptime monitoring (97% target)
  - Maintenance scheduling
  - Data quality checks

- **User Management**
  - Approve new officer registrations
  - Assign farmers to officers
  - Deactivate accounts
  - Role modifications
  - Audit logs

### 5. Community Hub Features
- **Q&A Forum**
  - Post questions
  - Answer questions
  - Upvote/downvote
  - Accept best answer
  - Expert verification badges
  - Tag system (crops, pests, soil, weather)
  - Search functionality

- **Knowledge Board**
  - Categorized articles (Crops, Pests, Weather, Soil, Equipment)
  - Rich text content with images
  - Save for later
  - Share articles
  - Reading time estimates
  - Expert-authored content

- **Direct Messaging**
  - One-on-one chat
  - Photo/file sharing
  - Online status indicators
  - Read receipts
  - Message notifications

### 6. Multi-Language & Accessibility
- **Bilingual Support** (English/Swahili initially)
- **Text-to-speech** for all major content
- **Icon-based navigation** (low literacy friendly)
- **Voice message recording**
- **Large touch targets** (44px minimum)
- **High contrast design** (WCAG AA compliant)
- **Offline capability** (future - PWA)

---

## 🛠️ Technology Stack

### Backend
```
Language:           Python 3.11+
Framework:          Django 5.0
REST API:           Django REST Framework (DRF) 3.14+
Authentication:     djangorestframework-simplejwt
Database:           PostgreSQL 15+
Cache:              Redis 7.0
Real-time:          Django Channels (WebSockets)
File Storage:       AWS S3 / Cloudinary
Task Queue:         Celery 5.3
Message Broker:     Redis / RabbitMQ
Admin Panel:        Django Admin (customized)
API Documentation:  drf-spectacular (OpenAPI 3.0)
```

### Frontend (Already Built)
```
Framework:          React 18.x
Language:           TypeScript 5.x
Styling:            Tailwind CSS 4.0
UI Components:      shadcn/ui
Icons:              Lucide React
Build Tool:         Vite 5.x
State Management:   React Hooks (+ Zustand future)
HTTP Client:        Axios
```

### External Services
```
SMS Gateway:        Africa's Talking API
Weather Data:       OpenWeatherMap API + Kenya Met Dept
Cloud Storage:      AWS S3 or Cloudinary
Maps:               Google Maps API / OpenStreetMap
Email:              SendGrid / AWS SES
Push Notifications: Firebase Cloud Messaging (FCM)
```

### Development Tools
```
Version Control:    Git + GitHub
API Testing:        Postman / Insomnia
Code Quality:       Black, Flake8, Pylint, mypy
Database Migration: Django Migrations
Environment:        python-decouple, python-dotenv
Documentation:      Swagger UI (drf-spectacular)
```

### Deployment
```
Hosting:            AWS / DigitalOcean / Heroku
Web Server:         Gunicorn
Reverse Proxy:      Nginx
Static Files:       AWS S3 + CloudFront / Whitenoise
Database:           AWS RDS PostgreSQL / Managed DB
Monitoring:         Sentry, New Relic
CI/CD:              GitHub Actions
Containerization:   Docker + Docker Compose
```

---

## 📊 Database Models

### User Management

#### 1. User Model (Extended AbstractUser)
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    # Roles
    FARMER = 'farmer'
    FIELD_OFFICER = 'officer'
    HQ_ANALYST = 'hq'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (FIELD_OFFICER, 'Field Officer'),
        (HQ_ANALYST, 'HQ Analyst'),
        (ADMIN, 'Administrator'),
    ]
    
    # Core fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    language_preference = models.CharField(max_length=2, default='en')  # en, sw
    
    # Location
    county = models.CharField(max_length=100, blank=True)
    sub_county = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Profile
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    # Settings
    notification_preferences = models.JSONField(default=dict)  # {app: True, sms: True, email: False}
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['county', 'sub_county']),
        ]
```

#### 2. FarmerProfile
```python
class FarmerProfile(models.Model):
    """
    Additional information specific to farmers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    
    # Farm details
    farm_name = models.CharField(max_length=200)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2)  # in acres
    farm_size_unit = models.CharField(max_length=10, default='acres')
    
    # Crops (many-to-many relationship)
    primary_crops = models.JSONField(default=list)  # ['maize', 'beans', 'tea']
    
    # Assigned officer
    assigned_officer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_farmers',
        limit_choices_to={'role': User.FIELD_OFFICER}
    )
    
    # Farming details
    farming_experience_years = models.PositiveIntegerField(null=True, blank=True)
    irrigation_method = models.CharField(max_length=50, blank=True)  # rain-fed, drip, sprinkler
    soil_type = models.CharField(max_length=50, blank=True)
    
    # Statistics
    total_reports_submitted = models.PositiveIntegerField(default=0)
    last_report_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farmer_profiles'
```

#### 3. FieldOfficerProfile
```python
class FieldOfficerProfile(models.Model):
    """
    Additional information specific to field officers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    
    # Professional details
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)  # "Agricultural Extension Officer"
    department = models.CharField(max_length=100)
    office_location = models.CharField(max_length=200)
    
    # Contact
    office_phone = models.CharField(max_length=15, blank=True)
    
    # Coverage area
    coverage_counties = models.JSONField(default=list)  # ['Trans-Nzoia']
    coverage_sub_counties = models.JSONField(default=list)
    
    # Working hours
    working_hours_start = models.TimeField(default='08:00')
    working_hours_end = models.TimeField(default='17:00')
    working_days = models.JSONField(default=list)  # ['monday', 'tuesday', ...]
    
    # Status
    is_available = models.BooleanField(default=True)
    current_status = models.CharField(max_length=50, default='available')  # available, busy, offline
    
    # Statistics
    total_farmers_assigned = models.PositiveIntegerField(default=0)
    total_reports_responded = models.PositiveIntegerField(default=0)
    average_response_time_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'officer_profiles'
```

### Observation & Reporting

#### 4. ObservationReport
```python
class ObservationReport(models.Model):
    """
    Farmer observation reports
    """
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_RESOLVED, 'Resolved'),
        (STATUS_CLOSED, 'Closed'),
    ]
    
    SEVERITY_MILD = 'mild'
    SEVERITY_MODERATE = 'moderate'
    SEVERITY_SEVERE = 'severe'
    SEVERITY_CRITICAL = 'critical'
    
    SEVERITY_CHOICES = [
        (SEVERITY_MILD, 'Mild'),
        (SEVERITY_MODERATE, 'Moderate'),
        (SEVERITY_SEVERE, 'Severe'),
        (SEVERITY_CRITICAL, 'Critical'),
    ]
    
    # Core fields
    report_id = models.CharField(max_length=20, unique=True, editable=False)  # Auto-generated
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observations')
    assigned_officer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_reports'
    )
    
    # Farm details
    farm_name = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=100)
    plot_size = models.DecimalField(max_digits=10, decimal_places=2)
    plot_size_unit = models.CharField(max_length=10, default='acres')
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_description = models.CharField(max_length=200, blank=True)
    
    # Observations
    observations = models.JSONField(default=list)  # ['yellow_leaves', 'dry_soil', 'pests_visible']
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    date_noticed = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.IntegerField(default=5)  # 1 (highest) to 10 (lowest)
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'observation_reports'
        ordering = ['-priority', '-submitted_at']
        indexes = [
            models.Index(fields=['farmer', 'status']),
            models.Index(fields=['assigned_officer', 'status']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['-submitted_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            # Generate unique report ID: RPT-YYYYMMDD-XXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_report = ObservationReport.objects.filter(
                report_id__startswith=f'RPT-{date_str}'
            ).order_by('-report_id').first()
            
            if last_report:
                last_num = int(last_report.report_id.split('-')[-1])
                new_num = str(last_num + 1).zfill(4)
            else:
                new_num = '0001'
            
            self.report_id = f'RPT-{date_str}-{new_num}'
        
        super().save(*args, **kwargs)
```

#### 5. ReportPhoto
```python
class ReportPhoto(models.Model):
    """
    Photos attached to observation reports
    """
    report = models.ForeignKey(ObservationReport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='reports/photos/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(null=True)  # in bytes
    
    class Meta:
        db_table = 'report_photos'
        ordering = ['uploaded_at']
```

#### 6. ReportVoiceNote
```python
class ReportVoiceNote(models.Model):
    """
    Voice notes attached to observation reports
    """
    report = models.OneToOneField(ObservationReport, on_delete=models.CASCADE, related_name='voice_note')
    audio_file = models.FileField(upload_to='reports/audio/%Y/%m/%d/')
    duration_seconds = models.PositiveIntegerField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(null=True)
    
    class Meta:
        db_table = 'report_voice_notes'
```

#### 7. OfficerResponse
```python
class OfficerResponse(models.Model):
    """
    Field officer responses to farmer reports
    """
    report = models.OneToOneField(ObservationReport, on_delete=models.CASCADE, related_name='response')
    officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    
    # Response content
    response_text = models.TextField()
    recommended_actions = models.JSONField(default=list)  # ["Apply fertilizer", "Water regularly"]
    
    # Follow-up
    site_visit_required = models.BooleanField(default=False)
    site_visit_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Metadata
    responded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'officer_responses'
```

### Weather & Alerts

#### 8. WeatherStation
```python
class WeatherStation(models.Model):
    """
    Weather stations across Kenya
    """
    STATUS_ACTIVE = 'active'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_OFFLINE = 'offline'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_MAINTENANCE, 'Maintenance'),
        (STATUS_OFFLINE, 'Offline'),
    ]
    
    # Identification
    station_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    
    # Location
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100, blank=True)
    location_description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.DecimalField(max_digits=7, decimal_places=2, null=True)  # meters above sea level
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    last_reading_at = models.DateTimeField(null=True, blank=True)
    
    # Management
    managed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='managed_stations'
    )
    
    # Metadata
    installed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'weather_stations'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['county']),
        ]
```

#### 9. WeatherData
```python
class WeatherData(models.Model):
    """
    Weather readings from stations
    """
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name='readings')
    
    # Timestamp
    reading_datetime = models.DateTimeField(db_index=True)
    
    # Temperature (°C)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Humidity (%)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Rainfall (mm)
    rainfall = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rainfall_24h = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # Cumulative 24h
    
    # Wind
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2)  # km/h
    wind_direction = models.CharField(max_length=3)  # N, NE, E, SE, S, SW, W, NW
    wind_gust = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    
    # Atmospheric
    pressure = models.DecimalField(max_digits=7, decimal_places=2, null=True)  # hPa
    
    # Cloud & Visibility
    cloud_cover = models.CharField(max_length=20, blank=True)  # clear, partly, cloudy, overcast
    visibility = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # km
    
    # Soil
    soil_moisture = models.CharField(max_length=20, blank=True)  # dry, moderate, wet
    soil_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Conditions
    weather_condition = models.CharField(max_length=100, blank=True)  # sunny, rainy, etc.
    
    # Additional data
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='weather_recordings'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'weather_data'
        ordering = ['-reading_datetime']
        indexes = [
            models.Index(fields=['station', '-reading_datetime']),
            models.Index(fields=['-reading_datetime']),
        ]
        unique_together = ['station', 'reading_datetime']
```

#### 10. WeatherForecast
```python
class WeatherForecast(models.Model):
    """
    Weather forecasts for locations
    """
    # Location reference
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name='forecasts')
    county = models.CharField(max_length=100)
    
    # Forecast details
    forecast_date = models.DateField(db_index=True)
    forecast_datetime = models.DateTimeField(null=True)  # For hourly forecasts
    
    # Temperature
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Conditions
    weather_condition = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Precipitation
    rain_probability = models.DecimalField(max_digits=5, decimal_places=2)  # %
    expected_rainfall = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # mm
    
    # Wind
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    wind_direction = models.CharField(max_length=3, blank=True)
    
    # Other
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cloud_cover = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # %
    
    # Data source
    source = models.CharField(max_length=100)  # 'OpenWeatherMap', 'Kenya Met', etc.
    
    # Metadata
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'weather_forecasts'
        ordering = ['forecast_date']
        indexes = [
            models.Index(fields=['county', 'forecast_date']),
            models.Index(fields=['station', 'forecast_date']),
        ]
```

#### 11. Alert
```python
class Alert(models.Model):
    """
    Alerts/advisories sent to users
    """
    TYPE_WEATHER = 'weather'
    TYPE_PEST = 'pest'
    TYPE_DISEASE = 'disease'
    TYPE_ADVISORY = 'advisory'
    TYPE_SYSTEM = 'system'
    
    TYPE_CHOICES = [
        (TYPE_WEATHER, 'Weather'),
        (TYPE_PEST, 'Pest'),
        (TYPE_DISEASE, 'Disease'),
        (TYPE_ADVISORY, 'Advisory'),
        (TYPE_SYSTEM, 'System'),
    ]
    
    SEVERITY_CRITICAL = 'critical'
    SEVERITY_HIGH = 'high'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_LOW = 'low'
    
    SEVERITY_CHOICES = [
        (SEVERITY_CRITICAL, 'Critical'),
        (SEVERITY_HIGH, 'High'),
        (SEVERITY_MEDIUM, 'Medium'),
        (SEVERITY_LOW, 'Low'),
    ]
    
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_SENT = 'sent'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_SENT, 'Sent'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    
    # Core fields
    alert_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    # Targeting
    target_regions = models.JSONField(default=list)  # ['Trans-Nzoia', 'Uasin Gishu']
    target_sub_counties = models.JSONField(default=list, blank=True)
    affected_crops = models.JSONField(default=list, blank=True)  # ['maize', 'beans']
    target_roles = models.JSONField(default=list)  # ['farmer', 'officer']
    
    # Delivery channels
    send_app_notification = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    
    # Status & Scheduling
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    total_recipients = models.PositiveIntegerField(default=0)
    total_delivered = models.PositiveIntegerField(default=0)
    total_read = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)
    
    # Creator
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='alerts_created')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_for']),
            models.Index(fields=['severity', 'status']),
        ]
```

#### 12. UserAlert
```python
class UserAlert(models.Model):
    """
    Alert delivery tracking for individual users
    """
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='user_alerts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_alerts')
    
    # Delivery status
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    
    # Timestamps
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_alerts'
        unique_together = ['alert', 'user']
        indexes = [
            models.Index(fields=['user', 'is_read', '-delivered_at']),
        ]
```

### Community Features

#### 13. Question
```python
class Question(models.Model):
    """
    Questions in Q&A forum
    """
    # Core fields
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    
    # Categorization
    tags = models.JSONField(default=list)  # ['pests', 'maize', 'control']
    category = models.CharField(max_length=100, blank=True)  # crops, pests, weather, soil
    
    # Status
    has_accepted_answer = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    upvote_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
```

#### 14. Answer
```python
class Answer(models.Model):
    """
    Answers to questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    
    # Content
    content = models.TextField()
    
    # Status
    is_accepted = models.BooleanField(default=False)
    is_expert_answer = models.BooleanField(default=False)  # Verified expert
    
    # Statistics
    upvote_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'answers'
        ordering = ['-is_accepted', '-upvote_count', '-created_at']
```

#### 15. KnowledgeArticle
```python
class KnowledgeArticle(models.Model):
    """
    Knowledge base articles
    """
    # Core fields
    title = models.CharField(max_length=300)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    
    # Categorization
    category = models.CharField(max_length=100)  # crops, pests, weather, soil, equipment
    tags = models.JSONField(default=list)
    
    # Featured image
    featured_image = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_expert_verified = models.BooleanField(default=False)
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    save_count = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Reading time
    reading_time_minutes = models.PositiveIntegerField(null=True)
    
    # Metadata
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'knowledge_articles'
        ordering = ['-published_at']
```

#### 16. Message
```python
class Message(models.Model):
    """
    Direct messages between users
    """
    # Participants
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    # Content
    content = models.TextField()
    
    # Attachments
    has_attachment = models.BooleanField(default=False)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_recipient = models.BooleanField(default=False)
    
    # Timestamps
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['sender', 'recipient', '-sent_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
```

---

## 🔌 API Endpoints

### Authentication Endpoints

```
POST   /api/v1/auth/register/              - User registration
POST   /api/v1/auth/login/                 - User login (JWT tokens)
POST   /api/v1/auth/logout/                - User logout
POST   /api/v1/auth/refresh/               - Refresh access token
POST   /api/v1/auth/verify-phone/          - Verify phone number (OTP)
POST   /api/v1/auth/forgot-password/       - Request password reset
POST   /api/v1/auth/reset-password/        - Reset password
GET    /api/v1/auth/me/                    - Get current user profile
PATCH  /api/v1/auth/me/                    - Update current user profile
```

### Farmer Endpoints

```
GET    /api/v1/farmers/dashboard/          - Get farmer dashboard data
GET    /api/v1/farmers/profile/            - Get farmer profile details
PATCH  /api/v1/farmers/profile/            - Update farmer profile

# Observations
GET    /api/v1/farmers/observations/       - List farmer's observations
POST   /api/v1/farmers/observations/       - Create new observation report
GET    /api/v1/farmers/observations/{id}/  - Get observation detail
PATCH  /api/v1/farmers/observations/{id}/  - Update observation (if pending)
DELETE /api/v1/farmers/observations/{id}/  - Delete observation (if pending)

# Report attachments
POST   /api/v1/farmers/observations/{id}/photos/      - Upload photo
DELETE /api/v1/farmers/observations/{id}/photos/{pid}/ - Delete photo
POST   /api/v1/farmers/observations/{id}/voice-note/  - Upload voice note

# Weather
GET    /api/v1/farmers/weather/current/    - Get current weather
GET    /api/v1/farmers/weather/forecast/   - Get weather forecast (4-7 days)

# Officer
GET    /api/v1/farmers/my-officer/         - Get assigned field officer details

# Alerts
GET    /api/v1/farmers/alerts/             - List farmer's alerts
GET    /api/v1/farmers/alerts/{id}/        - Get alert detail
PATCH  /api/v1/farmers/alerts/{id}/read/   - Mark alert as read
```

### Field Officer Endpoints

```
GET    /api/v1/officers/dashboard/         - Get officer dashboard data
GET    /api/v1/officers/profile/           - Get officer profile
PATCH  /api/v1/officers/profile/           - Update officer profile

# Farmer management
GET    /api/v1/officers/farmers/           - List assigned farmers
GET    /api/v1/officers/farmers/{id}/      - Get farmer details
GET    /api/v1/officers/farmers/{id}/reports/ - Get farmer's report history

# Reports
GET    /api/v1/officers/reports/           - List farmer reports (filterable)
GET    /api/v1/officers/reports/{id}/      - Get report detail
PATCH  /api/v1/officers/reports/{id}/      - Update report status
POST   /api/v1/officers/reports/{id}/respond/ - Respond to report
POST   /api/v1/officers/reports/{id}/visit/  - Schedule site visit

# Weather stations
GET    /api/v1/officers/weather-stations/  - List managed stations
GET    /api/v1/officers/weather-stations/{id}/ - Get station details
POST   /api/v1/officers/weather-data/      - Submit weather reading
GET    /api/v1/officers/weather-data/      - List weather readings

# Analytics
GET    /api/v1/officers/analytics/area/    - Get area performance metrics
GET    /api/v1/officers/analytics/reports/ - Get report statistics
```

### HQ Endpoints

```
GET    /api/v1/hq/dashboard/               - Get system overview
GET    /api/v1/hq/analytics/regional/      - Regional performance data
GET    /api/v1/hq/analytics/trends/        - Weather/agricultural trends

# Alerts
GET    /api/v1/hq/alerts/                  - List all alerts
POST   /api/v1/hq/alerts/                  - Create alert
GET    /api/v1/hq/alerts/{id}/             - Get alert details
PATCH  /api/v1/hq/alerts/{id}/             - Update alert
DELETE /api/v1/hq/alerts/{id}/             - Delete alert
POST   /api/v1/hq/alerts/{id}/broadcast/   - Broadcast alert
GET    /api/v1/hq/alerts/{id}/delivery-status/ - Get delivery stats

# Alert templates
GET    /api/v1/hq/alert-templates/         - List templates
POST   /api/v1/hq/alert-templates/         - Create template
GET    /api/v1/hq/alert-templates/{id}/    - Get template
PATCH  /api/v1/hq/alert-templates/{id}/    - Update template
DELETE /api/v1/hq/alert-templates/{id}/    - Delete template

# Weather stations
GET    /api/v1/hq/weather-stations/        - List all stations
POST   /api/v1/hq/weather-stations/        - Add new station
GET    /api/v1/hq/weather-stations/{id}/   - Get station details
PATCH  /api/v1/hq/weather-stations/{id}/   - Update station
GET    /api/v1/hq/weather-stations/{id}/status/ - Get status & readings

# User management
GET    /api/v1/hq/users/                   - List all users (paginated)
GET    /api/v1/hq/users/{id}/              - Get user details
PATCH  /api/v1/hq/users/{id}/              - Update user
POST   /api/v1/hq/users/{id}/deactivate/  - Deactivate user
POST   /api/v1/hq/users/{id}/activate/    - Activate user

# System health
GET    /api/v1/hq/system/health/           - System health status
GET    /api/v1/hq/system/logs/             - Activity logs
```

### Community Endpoints

```
# Q&A Forum
GET    /api/v1/community/questions/        - List questions (paginated, filterable)
POST   /api/v1/community/questions/        - Create question
GET    /api/v1/community/questions/{id}/   - Get question detail
PATCH  /api/v1/community/questions/{id}/   - Update question
DELETE /api/v1/community/questions/{id}/   - Delete question

POST   /api/v1/community/questions/{id}/answers/     - Post answer
GET    /api/v1/community/questions/{id}/answers/     - List answers
PATCH  /api/v1/community/answers/{id}/               - Update answer
DELETE /api/v1/community/answers/{id}/               - Delete answer
POST   /api/v1/community/answers/{id}/accept/        - Accept answer
POST   /api/v1/community/answers/{id}/upvote/        - Upvote answer
POST   /api/v1/community/answers/{id}/downvote/      - Downvote answer

# Knowledge Base
GET    /api/v1/community/articles/         - List articles
POST   /api/v1/community/articles/         - Create article (HQ/Officer only)
GET    /api/v1/community/articles/{id}/    - Get article
PATCH  /api/v1/community/articles/{id}/    - Update article
DELETE /api/v1/community/articles/{id}/    - Delete article
POST   /api/v1/community/articles/{id}/save/ - Save article for later
POST   /api/v1/community/articles/{id}/helpful/ - Mark as helpful

# Messaging
GET    /api/v1/community/conversations/    - List conversations
GET    /api/v1/community/conversations/{user_id}/ - Get conversation with user
POST   /api/v1/community/messages/         - Send message
GET    /api/v1/community/messages/{id}/    - Get message
PATCH  /api/v1/community/messages/{id}/read/ - Mark as read
```

### Utility Endpoints

```
GET    /api/v1/utils/counties/             - List Kenya counties
GET    /api/v1/utils/crops/                - List supported crops
GET    /api/v1/utils/observation-types/    - List observation options
GET    /api/v1/utils/search/               - Global search
```

---

## 🌐 External APIs

### 1. OpenWeatherMap API
```
Purpose: Weather data & forecasts
Endpoint: https://api.openweathermap.org/data/2.5/
Key Features:
  - Current weather data
  - 5-day / 3-hour forecast
  - 16-day daily forecast
  - Historical data

Endpoints Used:
  - /weather              (Current weather)
  - /forecast             (5-day forecast)
  - /onecall             (One call API - current + forecast)

Rate Limits: 1,000 calls/day (free tier)
Cost: Free tier available, paid plans for higher limits
```

### 2. Kenya Meteorological Department API
```
Purpose: Local weather data (if available)
Endpoint: [To be confirmed with Kenya Met]
Data: 
  - Weather station readings
  - Local forecasts
  - Agricultural advisories
  - Seasonal predictions

Integration: Primary data source, fallback to OpenWeather
```

### 3. Africa's Talking SMS API
```
Purpose: SMS notifications
Endpoint: https://api.africastalking.com/version1/
Key Features:
  - Send SMS
  - Bulk SMS
  - Delivery reports
  - Premium SMS

Endpoints Used:
  - POST /messaging        (Send SMS)
  - GET  /messaging        (Fetch messages)
  - GET  /messaging/delivery (Delivery reports)

Rate Limits: Based on account credits
Cost: ~$0.01 per SMS in Kenya
```

### 4. Cloudinary / AWS S3
```
Purpose: Image & file storage
Features:
  - Image upload
  - Image transformations
  - CDN delivery
  - Video/audio storage

Cloudinary API:
  - POST /upload          (Upload files)
  - Automatic optimization
  - Image transformations (resize, crop, etc.)

Rate Limits: Based on plan (free tier: 25 credits/month)
```

### 5. Firebase Cloud Messaging (FCM)
```
Purpose: Push notifications
Endpoint: https://fcm.googleapis.com/
Features:
  - Push notifications to mobile/web
  - Topic-based messaging
  - Device group messaging
  - Analytics

Integration: Send alerts to farmers/officers in real-time
Rate Limits: Unlimited (free)
```

### 6. Google Maps API (Optional)
```
Purpose: Location services
Features:
  - Geocoding (address → coordinates)
  - Reverse geocoding (coordinates → address)
  - Distance calculations
  - Maps display

Endpoints:
  - /geocode/json         (Geocoding)
  - /distancematrix/json  (Distance calculations)

Rate Limits: $200 free credit/month
```

---

## 📅 5-Week Development Plan

### Week 1: Project Setup & Core Backend (Nov 25 - Dec 1)

#### Days 1-2: Project Initialization
- [ ] Initialize Django project
  - Create virtual environment
  - Install Django 5.0, DRF, PostgreSQL adapter
  - Set up project structure
  - Configure settings (development, staging, production)
  - Set up environment variables (.env)
  
- [ ] Database setup
  - Install PostgreSQL locally
  - Create database
  - Configure Django database settings
  - Set up Redis for caching

- [ ] Git & version control
  - Initialize git repository
  - Create .gitignore
  - Set up GitHub repository
  - Create initial commit
  - Set up branch protection rules

#### Days 3-4: User Authentication System
- [ ] Implement custom User model
  - Extend AbstractUser
  - Add role field (Farmer, Officer, HQ)
  - Add phone number field
  - Add location fields
  - Create migrations

- [ ] JWT Authentication
  - Install djangorestframework-simplejwt
  - Configure JWT settings
  - Create authentication endpoints
    - Register
    - Login
    - Logout
    - Token refresh
  - Add phone number verification (OTP via SMS)

- [ ] Profile models
  - FarmerProfile model
  - FieldOfficerProfile model
  - Create serializers
  - Create profile endpoints

#### Days 5-7: Core Models & Basic CRUD
- [ ] Implement core models
  - ObservationReport model
  - ReportPhoto model
  - ReportVoiceNote model
  - OfficerResponse model
  - Create migrations
  - Run migrations

- [ ] Create model serializers
  - ObservationReportSerializer
  - UserSerializer
  - ProfileSerializers

- [ ] Basic CRUD endpoints
  - Create observation report
  - List observations
  - Get observation detail
  - Update observation (pending only)
  
- [ ] File upload handling
  - Configure media files
  - Set up Cloudinary/S3 (if using)
  - Image upload endpoint
  - Voice note upload endpoint

**Week 1 Deliverables:**
✅ Django project fully configured
✅ User authentication working (JWT)
✅ Core models created and migrated
✅ Basic observation CRUD endpoints
✅ File upload capability

---

### Week 2: Weather & Alert Systems (Dec 2 - Dec 8)

#### Days 1-2: Weather Models & Integration
- [ ] Weather models
  - WeatherStation model
  - WeatherData model
  - WeatherForecast model
  - Create migrations

- [ ] OpenWeatherMap integration
  - Get API key
  - Create weather service class
  - Implement current weather fetch
  - Implement forecast fetch
  - Handle API errors

- [ ] Weather endpoints
  - GET current weather by location
  - GET weather forecast
  - GET weather by station
  - POST weather data (for officers)

#### Days 3-4: Alert System
- [ ] Alert models
  - Alert model
  - UserAlert model (delivery tracking)
  - AlertTemplate model
  - Create migrations

- [ ] Alert service
  - Create alert broadcasting logic
  - User targeting (by region, role, crops)
  - Delivery tracking
  - Alert expiration handling

- [ ] Alert endpoints
  - Create alert (HQ only)
  - List alerts
  - Get alert detail
  - Broadcast alert
  - Get delivery status
  - Mark alert as read

#### Days 5-7: Notification System
- [ ] SMS integration (Africa's Talking)
  - Get API credentials
  - Create SMS service class
  - Implement send SMS
  - Handle delivery reports
  - Test with real phone numbers

- [ ] Push notifications (FCM)
  - Set up Firebase project
  - Install Firebase Admin SDK
  - Create notification service
  - Send push notifications
  - Handle device token registration

- [ ] Celery setup for async tasks
  - Install Celery
  - Configure Celery with Redis
  - Create tasks
    - Send SMS task
    - Send push notification task
    - Fetch weather data task
  - Set up Celery beat for scheduled tasks

**Week 2 Deliverables:**
✅ Weather data fetching from OpenWeather
✅ Weather endpoints working
✅ Alert system implemented
✅ SMS notifications working
✅ Push notifications configured
✅ Celery async tasks running

---

### Week 3: Field Officer & HQ Features (Dec 9 - Dec 15)

#### Days 1-2: Field Officer Features
- [ ] Officer dashboard endpoint
  - Aggregate stats (farmers, reports, stations)
  - Pending reports
  - Priority tasks
  - Area metrics

- [ ] Farmer management
  - List assigned farmers
  - Get farmer details
  - Farmer report history
  - Assign farmer to officer (HQ function)

- [ ] Report management
  - List reports with filters (status, priority, date)
  - Get report detail
  - Respond to report
  - Update report status
  - Schedule site visit

- [ ] Weather station management
  - List managed stations
  - Submit weather readings
  - View historical data
  - Station status updates

#### Days 3-4: HQ Analytics
- [ ] HQ dashboard endpoint
  - System-wide statistics
  - Regional performance data
  - Critical alerts summary
  - Activity feed

- [ ] Analytics endpoints
  - Regional performance
  - Weather trends (charts data)
  - Report statistics
  - Officer performance
  - Station uptime metrics

- [ ] System health monitoring
  - API health check
  - Database health check
  - External services status
  - Error logging

#### Days 5-7: Admin Features
- [ ] User management (HQ)
  - List all users
  - Filter users (role, location, status)
  - User detail view
  - Activate/deactivate users
  - Approve officer registrations

- [ ] Station management (HQ)
  - Add new station
  - Update station details
  - Set station status
  - Assign station manager

- [ ] Data export
  - Export reports to CSV
  - Export weather data
  - Export user lists
  - Generate PDF reports

**Week 3 Deliverables:**
✅ Field officer dashboard complete
✅ Report response system working
✅ HQ analytics dashboard
✅ User management features
✅ Data export functionality

---

### Week 4: Community Features & Frontend Integration (Dec 16 - Dec 22)

#### Days 1-2: Community Models & Endpoints
- [ ] Q&A Forum models
  - Question model
  - Answer model
  - Vote model
  - Create migrations

- [ ] Q&A endpoints
  - List questions (with pagination, filters)
  - Create question
  - Post answer
  - Accept answer
  - Upvote/downvote
  - Search questions

#### Days 2-3: Knowledge Base & Messaging
- [ ] Knowledge base
  - KnowledgeArticle model
  - Article endpoints (CRUD)
  - Category filtering
  - Save article
  - Mark helpful

- [ ] Direct messaging
  - Message model
  - MessageAttachment model
  - Send message endpoint
  - List conversations
  - Get conversation messages
  - Mark as read

#### Days 4-7: Frontend Integration
- [ ] Connect React frontend to Django backend
  - Update API service layer
  - Replace mock data with real API calls
  - Add authentication headers
  - Handle API errors

- [ ] Authentication flow
  - Login page integration
  - Register page integration
  - Token management (localStorage)
  - Auto-refresh tokens
  - Logout functionality

- [ ] Farmer dashboard integration
  - Fetch dashboard data
  - Display weather
  - Show alerts
  - Observation form submission
  - File uploads (photos, voice)

- [ ] Officer dashboard integration
  - Fetch reports
  - Display reports with filters
  - Respond to reports
  - Submit weather data

- [ ] HQ dashboard integration
  - Fetch analytics
  - Display charts
  - Alert broadcasting
  - User management

**Week 4 Deliverables:**
✅ Community features (Q&A, Knowledge, Messaging)
✅ Frontend fully connected to backend
✅ Real authentication working
✅ All dashboards using real data
✅ File uploads working

---

### Week 5: Testing, Polish & Deployment (Dec 23 - Dec 29)

#### Days 1-2: Testing
- [ ] API testing
  - Write unit tests for models
  - Write tests for serializers
  - Write tests for views
  - Test authentication
  - Test permissions
  - Aim for 70%+ coverage

- [ ] Integration testing
  - Test complete user flows
  - Test file uploads
  - Test external API integrations
  - Test SMS sending
  - Test notifications

- [ ] Frontend testing
  - Test user flows
  - Test API integration
  - Test error handling
  - Cross-browser testing
  - Mobile responsiveness

#### Days 3-4: Performance & Security
- [ ] Performance optimization
  - Database query optimization
  - Add database indexes
  - Implement caching (Redis)
  - Optimize image uploads
  - API response optimization

- [ ] Security hardening
  - Set up CORS properly
  - Configure CSRF protection
  - Validate all inputs
  - Set up rate limiting
  - Environment variable security
  - SQL injection prevention

- [ ] Monitoring & logging
  - Set up Sentry for error tracking
  - Configure Django logging
  - API request logging
  - Set up alerts for errors

#### Days 5-7: Deployment
- [ ] Prepare for production
  - Update settings for production
  - Collect static files
  - Set up environment variables
  - Create requirements.txt
  - Update .gitignore

- [ ] Database setup
  - Set up production database (AWS RDS / DigitalOcean)
  - Run migrations on production
  - Create superuser
  - Backup strategy

- [ ] Deploy backend
  - Choose platform (Heroku / DigitalOcean / AWS)
  - Set up server (Gunicorn + Nginx)
  - Configure domain
  - Set up SSL certificate
  - Deploy Django app

- [ ] Deploy frontend
  - Build React app (npm run build)
  - Deploy to Vercel/Netlify
  - Configure environment variables
  - Connect to backend API
  - Test production deployment

- [ ] Final testing
  - Test all features in production
  - Test on mobile devices
  - Test SMS notifications
  - Test file uploads to S3/Cloudinary
  - Fix any issues

**Week 5 Deliverables:**
✅ Comprehensive test suite
✅ Performance optimized
✅ Security hardened
✅ Backend deployed and running
✅ Frontend deployed and connected
✅ Production ready!

---

## 📂 Project Structure

### Django Backend Structure

```
croppulse_backend/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── config/                          # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base settings
│   │   ├── development.py          # Dev settings
│   │   ├── production.py           # Prod settings
│   │   └── test.py                 # Test settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI config
│   └── asgi.py                     # ASGI config (for WebSockets)
│
├── apps/                            # Django apps
│   │
│   ├── users/                       # User management
│   │   ├── __init__.py
│   │   ├── models.py               # User, FarmerProfile, OfficerProfile
│   │   ├── serializers.py          # User serializers
│   │   ├── views.py                # Authentication views
│   │   ├── urls.py                 # User URLs
│   │   ├── admin.py                # Django admin config
│   │   ├── permissions.py          # Custom permissions
│   │   ├── managers.py             # Custom model managers
│   │   └── tests.py
│   │
│   ├── observations/                # Observation reports
│   │   ├── models.py               # ObservationReport, Photos, Voice
│   │   ├── serializers.py
│   │   ├── views.py                # Report CRUD
│   │   ├── urls.py
│   │   ├── filters.py              # DRF filters
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── weather/                     # Weather data
│   │   ├── models.py               # WeatherStation, WeatherData, Forecast
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py             # OpenWeather integration
│   │   ├── tasks.py                # Celery tasks
│   │   └── tests.py
│   │
│   ├── alerts/                      # Alert system
│   │   ├── models.py               # Alert, UserAlert
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py             # Alert broadcasting logic
│   │   ├── tasks.py                # Notification tasks
│   │   └── tests.py
│   │
│   ├── community/                   # Community features
│   │   ├── models.py               # Question, Answer, Article, Message
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   └── analytics/                   # Analytics & reporting
│       ├── views.py                # Analytics endpoints
│       ├── urls.py
│       ├── services.py             # Analytics calculations
│       └── tests.py
│
├── core/                            # Core utilities
│   ├── __init__.py
│   ├── exceptions.py               # Custom exceptions
│   ├── pagination.py               # Custom pagination
│   ├── permissions.py              # Base permissions
│   ├── utils.py                    # Utility functions
│   └── validators.py               # Custom validators
│
├── services/                        # External services
│   ├── __init__.py
│   ├── sms.py                      # Africa's Talking SMS
│   ├── notifications.py            # Push notifications (FCM)
│   ├── storage.py                  # S3/Cloudinary
│   ├── weather_api.py              # Weather API client
│   └── geocoding.py                # Google Maps API
│
├── media/                           # Uploaded files (dev only)
│   ├── avatars/
│   ├── reports/
│   │   ├── photos/
│   │   └── audio/
│   └── articles/
│
└── static/                          # Static files
    ├── admin/
    └── api/
```

### React Frontend Structure (Already exists)

```
croppulse_frontend/
│
├── src/
│   ├── components/
│   ├── services/                    # API services
│   │   ├── api.ts                  # Axios instance
│   │   ├── auth.ts                 # Auth API
│   │   ├── farmers.ts              # Farmer API
│   │   ├── officers.ts             # Officer API
│   │   ├── hq.ts                   # HQ API
│   │   └── community.ts            # Community API
│   ├── hooks/
│   ├── utils/
│   ├── types/
│   ├── contexts/
│   └── App.tsx
│
└── [Rest of frontend structure as documented]
```

---

## 🔐 Security & Authentication

### Authentication Strategy

1. **JWT (JSON Web Tokens)**
   - Access token (short-lived: 15 minutes)
   - Refresh token (longer-lived: 7 days)
   - Tokens stored in localStorage (frontend)
   - HttpOnly cookies option (more secure)

2. **Phone Verification**
   - OTP sent via SMS
   - 6-digit code
   - 5-minute expiration
   - Rate limiting (3 attempts)

3. **Password Requirements**
   - Minimum 8 characters
   - Must contain: letters, numbers
   - Optional: special characters

### Authorization (RBAC)

```python
# Permission classes
class IsFarmer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'farmer'

class IsFieldOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'officer'

class IsHQ(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'hq'

# Usage in views
class ObservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsFarmer]
```

### Security Measures

1. **Input Validation**
   - DRF serializer validation
   - Custom validators
   - Sanitize HTML inputs

2. **Rate Limiting**
   - Django-ratelimit
   - Per-user and per-IP limits
   - API: 100 requests/hour
   - Auth: 5 attempts/hour

3. **CORS Configuration**
   - Whitelist frontend domain
   - Allowed methods
   - Credentials support

4. **SQL Injection Prevention**
   - Django ORM (parameterized queries)
   - Never use raw SQL with user input

5. **XSS Prevention**
   - Django auto-escaping
   - DRF serializers
   - Content Security Policy

6. **File Upload Security**
   - File type validation
   - File size limits (5MB images, 2MB audio)
   - Virus scanning (ClamAV - optional)
   - Store in S3 (not on server)

---

## 🚀 Deployment Strategy

### Development Environment
```
Local machine
├── Django dev server (port 8000)
├── PostgreSQL (local)
├── Redis (local)
├── Celery worker (local)
└── React dev server (port 3000)
```

### Production Environment

```
                    Internet
                       │
                       ▼
                 ┌──────────┐
                 │   DNS    │
                 └──────────┘
                       │
           ┌───────────┼───────────┐
           │                       │
           ▼                       ▼
    ┌──────────┐           ┌──────────┐
    │ Frontend │           │ Backend  │
    │  Vercel  │           │  Server  │
    └──────────┘           └──────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌─────────┐  ┌─────────┐  ┌─────────┐
              │   DB    │  │  Redis  │  │   S3    │
              │   RDS   │  │         │  │         │
              └─────────┘  └─────────┘  └─────────┘
```

### Deployment Platforms (Options)

#### Option 1: Heroku (Easiest)
```
✅ Pros:
  - Easy deployment
  - Managed PostgreSQL
  - Managed Redis
  - Free tier available
  - Auto-scaling

❌ Cons:
  - More expensive at scale
  - US/EU data centers only
```

#### Option 2: DigitalOcean (Recommended)
```
✅ Pros:
  - Affordable ($5-10/month start)
  - Good for Kenya (SG/EU data centers)
  - Managed databases available
  - App Platform for easy deployment

❌ Cons:
  - Requires some server management
```

#### Option 3: AWS (Most Scalable)
```
✅ Pros:
  - Highly scalable
  - Most features
  - Global presence
  - Free tier (12 months)

❌ Cons:
  - Complex setup
  - Can be expensive
  - Steeper learning curve
```

### Deployment Checklist

```bash
# Backend Deployment
✅ Environment variables set
✅ Database migrated
✅ Static files collected
✅ Gunicorn configured
✅ Nginx configured
✅ SSL certificate installed
✅ Celery worker running
✅ Redis configured
✅ S3 bucket created
✅ DNS configured

# Frontend Deployment
✅ Environment variables set
✅ API URL configured
✅ Build completed
✅ Deployed to Vercel/Netlify
✅ Custom domain configured
✅ SSL certificate (auto)

# External Services
✅ Africa's Talking account
✅ OpenWeather API key
✅ Cloudinary account
✅ Firebase project
✅ Sentry account
```

---

## 📊 Success Metrics

### Technical Metrics
- API response time: < 200ms (95th percentile)
- Database query time: < 50ms average
- Uptime: 99.5%+
- Error rate: < 0.1%

### User Metrics
- Farmer registrations: 100 in first month
- Daily active users: 30%+ of registered
- Report submission: 3+ reports/farmer/month
- Officer response time: < 2 hours average
- Alert delivery rate: 95%+

### Business Metrics
- Farmer satisfaction: 80%+ positive feedback
- Crop loss prevention: Target 25% reduction
- System adoption: 5+ counties in 6 months

---

## 🎯 Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits exceeded | Medium | High | Implement caching, use multiple API keys |
| Database performance issues | Low | High | Proper indexing, query optimization |
| File storage costs high | Medium | Medium | Image compression, CDN, tiered storage |
| SMS costs exceed budget | Medium | High | Batch SMS, prioritize critical alerts |
| Server downtime | Low | Critical | Load balancing, auto-scaling, backups |

### External Dependencies

| Dependency | Risk | Backup Plan |
|------------|------|-------------|
| OpenWeather API | Service outage | Cache recent data, use Kenya Met |
| Africa's Talking | SMS failure | Email fallback, app notifications |
| Cloudinary/S3 | Service outage | Local storage backup |
| PostgreSQL host | Database failure | Daily backups, standby replica |

---

## 📝 Additional Considerations

### Data Privacy & Compliance
- **Kenya Data Protection Act** compliance
- Minimal PII collection
- User consent for data processing
- Right to data deletion
- Data encryption at rest and in transit

### Localization
- English and Swahili languages
- Kenya-specific date/time formats
- Kenya shillings (KES) for any payments
- Kenyan counties and locations

### Accessibility
- WCAG 2.1 AA compliance
- Screen reader support
- High contrast mode
- Large touch targets (44px)
- Icon + text labels

### Future Enhancements (Post-MVP)
- [ ] Mobile apps (React Native)
- [ ] Offline mode (PWA)
- [ ] AI crop disease detection
- [ ] Predictive analytics
- [ ] Satellite imagery integration
- [ ] IoT sensor integration
- [ ] Marketplace features
- [ ] Crop insurance integration
- [ ] Financial services integration

---

## 📞 Support & Resources

### Documentation
- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/

### Community
- Django Discord
- Stack Overflow
- Reddit r/django
- Dev.to Django community

### Kenya-Specific Resources
- Kenya Meteorological Department
- Ministry of Agriculture
- County agricultural offices
- Farmer cooperatives

---

## ✅ Pre-Development Checklist

Before starting development, ensure:

- [ ] PostgreSQL installed locally
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed (for frontend)
- [ ] Git installed and configured
- [ ] GitHub account set up
- [ ] Africa's Talking account created
- [ ] OpenWeatherMap API key obtained
- [ ] Cloudinary account created (or AWS S3)
- [ ] Text editor / IDE set up (VS Code recommended)
- [ ] Postman/Insomnia installed for API testing
- [ ] Project plan reviewed and understood

---

## 🎉 Project Completion Criteria

The project will be considered complete when:

✅ All three user dashboards are functional
✅ Authentication and authorization working
✅ Observation reporting system complete
✅ Weather data integration working
✅ Alert system operational
✅ SMS notifications working
✅ Community features implemented
✅ Frontend fully integrated with backend
✅ Comprehensive testing completed
✅ Deployed to production
✅ Documentation complete
✅ Initial user feedback collected

---

**Project Timeline:** 5 Weeks (Nov 25 - Dec 29, 2024)

**Target Launch Date:** January 1, 2025

**Post-Launch Support:** Ongoing maintenance and feature additions

---

*This document will be updated as the project progresses. All team members should review and provide feedback before development begins.*

**Last Updated:** November 22, 2024
**Version:** 1.0
**Status:** Ready for Development

---

## 📧 Contact

**Project Lead:** [Your Name]
**Email:** [your.email@example.com]
**GitHub:** [github.com/yourusername]
**Phone:** [Your Phone]

---

**Let's build CropPulse Africa and transform Kenyan agriculture!** 🌾🚀
