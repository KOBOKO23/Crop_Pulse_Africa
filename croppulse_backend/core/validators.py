"""
Custom validators for CropPulse Africa
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image
import magic


def validate_kenya_phone_number(value):
    """Validate Kenyan phone number format"""
    # Kenya phone numbers: +254XXXXXXXXX or 07XXXXXXXX or 01XXXXXXXX
    pattern = r'^(\+254|0)[17]\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid Kenyan phone number format. Use +254XXXXXXXXX or 07/01XXXXXXXX'),
            code='invalid_phone'
        )


def validate_latitude(value):
    """Validate latitude is within Kenya's approximate bounds"""
    if not (-5.0 <= value <= 5.5):
        raise ValidationError(
            _('Latitude must be within Kenya bounds (-5.0 to 5.5)'),
            code='invalid_latitude'
        )


def validate_longitude(value):
    """Validate longitude is within Kenya's approximate bounds"""
    if not (33.5 <= value <= 42.0):
        raise ValidationError(
            _('Longitude must be within Kenya bounds (33.5 to 42.0)'),
            code='invalid_longitude'
        )


def validate_image_file(file):
    """Validate uploaded file is a valid image"""
    try:
        # Check file size (max 10MB)
        if file.size > 10 * 1024 * 1024:
            raise ValidationError(
                _('Image file size cannot exceed 10MB'),
                code='file_too_large'
            )
        
        # Verify it's actually an image
        img = Image.open(file)
        img.verify()
        
        # Check mime type
        file.seek(0)
        mime = magic.from_buffer(file.read(1024), mime=True)
        if mime not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']:
            raise ValidationError(
                _('Unsupported image format. Use JPEG, PNG, or WebP'),
                code='invalid_format'
            )
        
        file.seek(0)
        
    except Exception as e:
        raise ValidationError(
            _('Invalid image file: %(error)s') % {'error': str(e)},
            code='invalid_image'
        )


def validate_audio_file(file):
    """Validate uploaded audio file"""
    # Check file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        raise ValidationError(
            _('Audio file size cannot exceed 5MB'),
            code='file_too_large'
        )
    
    # Check extension
    allowed_extensions = ['.mp3', '.wav', '.ogg', '.m4a']
    ext = file.name.lower().split('.')[-1]
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(
            _('Unsupported audio format. Use MP3, WAV, OGG, or M4A'),
            code='invalid_format'
        )


def validate_farm_size(value):
    """Validate farm size is reasonable (in hectares)"""
    if value <= 0:
        raise ValidationError(
            _('Farm size must be greater than 0'),
            code='invalid_size'
        )
    
    if value > 10000:  # 10,000 hectares seems like a reasonable max for small-holder farms
        raise ValidationError(
            _('Farm size seems unreasonably large. Please verify.'),
            code='size_too_large'
        )


def validate_temperature(value):
    """Validate temperature reading is reasonable for Kenya"""
    if not (-10 <= value <= 60):
        raise ValidationError(
            _('Temperature must be between -10°C and 60°C'),
            code='invalid_temperature'
        )


def validate_rainfall(value):
    """Validate rainfall reading is reasonable"""
    if value < 0:
        raise ValidationError(
            _('Rainfall cannot be negative'),
            code='invalid_rainfall'
        )
    
    if value > 500:  # 500mm in a day would be extreme
        raise ValidationError(
            _('Rainfall value seems unreasonably high. Please verify.'),
            code='rainfall_too_high'
        )


def validate_humidity(value):
    """Validate humidity percentage"""
    if not (0 <= value <= 100):
        raise ValidationError(
            _('Humidity must be between 0 and 100 percent'),
            code='invalid_humidity'
        )


def validate_wind_speed(value):
    """Validate wind speed is reasonable"""
    if value < 0:
        raise ValidationError(
            _('Wind speed cannot be negative'),
            code='invalid_wind_speed'
        )
    
    if value > 200:  # km/h
        raise ValidationError(
            _('Wind speed seems unreasonably high. Please verify.'),
            code='wind_speed_too_high'
        )


def validate_county_name(value):
    """Validate county name is a valid Kenyan county"""
    KENYA_COUNTIES = [
        'Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita-Taveta',
        'Garissa', 'Wajir', 'Mandera', 'Marsabit', 'Isiolo', 'Meru',
        'Tharaka-Nithi', 'Embu', 'Kitui', 'Machakos', 'Makueni', 'Nyandarua',
        'Nyeri', 'Kirinyaga', 'Murang\'a', 'Kiambu', 'Turkana', 'West Pokot',
        'Samburu', 'Trans-Nzoia', 'Uasin Gishu', 'Elgeyo-Marakwet', 'Nandi',
        'Baringo', 'Laikipia', 'Nakuru', 'Narok', 'Kajiado', 'Kericho',
        'Bomet', 'Kakamega', 'Vihiga', 'Bungoma', 'Busia', 'Siaya', 'Kisumu',
        'Homa Bay', 'Migori', 'Kisii', 'Nyamira', 'Nairobi'
    ]
    
    if value not in KENYA_COUNTIES:
        raise ValidationError(
            _('Invalid Kenyan county name'),
            code='invalid_county'
        )


def validate_crop_type(value):
    """Validate crop type is from the allowed list"""
    ALLOWED_CROPS = [
        'maize', 'wheat', 'rice', 'beans', 'peas', 'sorghum', 'millet',
        'cassava', 'sweet_potato', 'irish_potato', 'banana', 'sugarcane',
        'coffee', 'tea', 'cotton', 'sunflower', 'groundnuts', 'soybeans',
        'vegetables', 'fruits', 'other'
    ]
    
    if value.lower() not in ALLOWED_CROPS:
        raise ValidationError(
            _('Invalid crop type. Please select from the allowed list.'),
            code='invalid_crop'
        )
