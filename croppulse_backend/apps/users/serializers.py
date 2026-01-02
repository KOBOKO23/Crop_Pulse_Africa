"""
Serializers for Users app
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, FarmerProfile, FieldOfficerProfile, Notification
from core.utils import generate_verification_code
import secrets


class FarmerProfileSerializer(serializers.ModelSerializer):
    """Serializer for farmer profile"""

    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'farm_name', 'farm_size', 'primary_crop', 'secondary_crops',
            'latitude', 'longitude', 'years_of_experience', 'farming_type',
            'has_irrigation', 'has_greenhouse', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FieldOfficerProfileSerializer(serializers.ModelSerializer):
    """Serializer for field officer profile"""

    supervisor_name = serializers.CharField(source='supervisor.full_name', read_only=True)

    class Meta:
        model = FieldOfficerProfile
        fields = [
            'id', 'employee_id', 'assigned_counties', 'assigned_subcounties',
            'supervisor', 'supervisor_name', 'coverage_area_radius',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    farmer_profile = FarmerProfileSerializer(read_only=True)
    field_officer_profile = FieldOfficerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'email', 'full_name', 'role',
            'profile_picture', 'county', 'subcounty', 'ward', 'village',
            'is_verified', 'language', 'receive_sms_notifications',
            'receive_push_notifications', 'fcm_token', 'created_at', 'updated_at',
            'last_login', 'farmer_profile', 'field_officer_profile'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at', 'last_login']
        extra_kwargs = {
            'fcm_token': {'write_only': True},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone_number', 'email', 'full_name', 'role', 'password',
            'password_confirm', 'county', 'language'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        # Generate verification code
        user.verification_code = generate_verification_code()
        user.verification_code_created_at = timezone.now()
        user.save()

        # Create role-specific profile safely
        if user.role == 'farmer':
            FarmerProfile.objects.get_or_create(
                user=user,
                defaults={'farm_size': 0, 'primary_crop': 'maize'}
            )
        elif user.role == 'field_officer':
            FieldOfficerProfile.objects.get_or_create(
                user=user,
                defaults={'employee_id': f'FO-{user.id:06d}'}
            )

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)

            if not user:
                raise serializers.ValidationError("Invalid credentials")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
        else:
            raise serializers.ValidationError("Must include phone number and password")

        data['user'] = user
        return data


class VerifyPhoneSerializer(serializers.Serializer):
    """Serializer for phone verification"""

    phone_number = serializers.CharField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.is_verified:
            raise serializers.ValidationError("Phone number already verified")

        if user.verification_code != data['verification_code']:
            raise serializers.ValidationError("Invalid verification code")

        # Check if code is expired (10 minutes)
        if user.verification_code_created_at:
            time_diff = timezone.now() - user.verification_code_created_at
            if time_diff.total_seconds() > 600:
                raise serializers.ValidationError("Verification code has expired")

        data['user'] = user
        return data


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resending verification code"""
    phone_number = serializers.CharField()


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""

    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'priority', 'title', 'message', 'data',
            'is_read', 'read_at', 'related_object_type', 'related_object_id',
            'sent_via_push', 'sent_via_sms', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'profile_picture', 'county', 'subcounty',
            'ward', 'village', 'language', 'receive_sms_notifications',
            'receive_push_notifications'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data


class UpdateFCMTokenSerializer(serializers.Serializer):
    """Serializer for updating FCM token"""
    fcm_token = serializers.CharField()


# -----------------------
# Simplified Farmer Auth
# -----------------------
class FarmerSimpleRegistrationSerializer(serializers.Serializer):
    """Minimal registration for farmers (SMS-based login)"""
    phone_number = serializers.CharField()
    full_name = serializers.CharField()
    county = serializers.CharField()
    language = serializers.CharField(default='en')

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered")
        return value

    def create(self, validated_data):
        # Auto-generate a strong random password
        random_password = secrets.token_urlsafe(32)

        # Ensure role is always 'farmer'
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            county=validated_data['county'],
            language=validated_data.get('language', 'en'),
            role='farmer',
            password=random_password
        )

        # Generate verification code
        user.verification_code = generate_verification_code()
        user.verification_code_created_at = timezone.now()
        user.save()

        # Safely create FarmerProfile with defaults to avoid validation errors
        FarmerProfile.objects.get_or_create(
            user=user,
            defaults={
                'farm_size': 0,
                'primary_crop': 'Unknown',
                'years_of_experience': 0,
                'farming_type': 'subsistence',
                'secondary_crops': [],
                'has_irrigation': False,
                'has_greenhouse': False,
                'latitude': None,
                'longitude': None
            }
        )

        return user


class FarmerSMSLoginRequestSerializer(serializers.Serializer):
    """Request OTP for farmer SMS login"""
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        try:
            user = User.objects.get(phone_number=value)
            if user.role != 'farmer':
                raise serializers.ValidationError(
                    "SMS login is only available for farmers. Please use password login."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError("Phone number not registered")
        return value


"""
Replace FarmerSMSLoginVerifySerializer in apps/users/serializers.py
with this version that has better error messages and logging
"""
import logging

logger = logging.getLogger(__name__)


class FarmerSMSLoginVerifySerializer(serializers.Serializer):
    """Verify OTP for farmer SMS login"""
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.CharField(required=True, min_length=6, max_length=6)

    def validate(self, data):
        """Validate OTP and user"""
        import logging
        logger = logging.getLogger(__name__)
        
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code', '').strip()
        
        logger.info("=" * 70)
        logger.info("🔐 OTP VERIFICATION")
        logger.info("=" * 70)
        logger.info(f"Phone: {phone_number}")
        logger.info(f"OTP: {otp_code}")
        
        # Find user
        try:
            user = User.objects.get(phone_number=phone_number)
            logger.info(f"✅ User found: {user.full_name}")
        except User.DoesNotExist:
            logger.error("❌ User not found")
            raise serializers.ValidationError("User not found")

        # Check role
        if user.role != 'farmer':
            logger.error(f"❌ Wrong role: {user.role}")
            raise serializers.ValidationError("SMS login only for farmers")

        # Log stored OTP
        logger.info(f"Stored OTP: '{user.verification_code}'")
        logger.info(f"Provided OTP: '{otp_code}'")
        logger.info(f"Match: {user.verification_code == otp_code}")
        
        # Check OTP match
        if not user.verification_code or user.verification_code != otp_code:
            logger.error("❌ OTP mismatch")
            raise serializers.ValidationError("Invalid OTP code")

        # Check expiration
        if user.verification_code_created_at:
            from django.utils import timezone
            elapsed = timezone.now() - user.verification_code_created_at
            age = elapsed.total_seconds()
            logger.info(f"OTP age: {age} seconds")
            
            if age > 600:
                logger.error("❌ OTP expired")
                raise serializers.ValidationError("OTP has expired")
            
            logger.info(f"✅ OTP valid ({600-age:.0f}s remaining)")
        else:
            logger.error("❌ No OTP timestamp")
            raise serializers.ValidationError("Invalid OTP state")

        logger.info("✅ All checks passed")
        logger.info("=" * 70)
        
        data['user'] = user
        return data

class OnboardingStatusSerializer(serializers.Serializer):
    """Serializer for checking user onboarding status"""
    has_profile_picture = serializers.BooleanField()
    has_location = serializers.BooleanField()
    has_farm_details = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    onboarding_complete = serializers.BooleanField()
    next_steps = serializers.ListField(child=serializers.CharField())


# Default serializer for OPTIONS requests
class AuthActionSerializer(serializers.Serializer):
    """
    Default serializer for ViewSets to handle OPTIONS preflight requests.
    Prevents AssertionError when serializer_class is not defined.
    """
    pass
