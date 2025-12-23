"""
Serializers for Users app
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, FarmerProfile, FieldOfficerProfile, Notification
from core.utils import generate_verification_code


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
            'receive_push_notifications', 'fcm_token', 'created_at',
            'updated_at', 'last_login', 'farmer_profile', 'field_officer_profile'
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
        
        # Create role-specific profile
        if user.role == 'farmer':
            FarmerProfile.objects.create(
                user=user,
                farm_size=0,
                primary_crop='maize'
            )
        elif user.role == 'field_officer':
            FieldOfficerProfile.objects.create(
                user=user,
                employee_id=f'FO-{user.id:06d}'
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
            if time_diff.total_seconds() > 600:  # 10 minutes
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


# New serializers for simplified farmer login
class FarmerSimpleRegistrationSerializer(serializers.Serializer):
    """Simplified registration for farmers - minimal fields"""
    
    phone_number = serializers.CharField()
    full_name = serializers.CharField()
    county = serializers.CharField()
    language = serializers.CharField(default='en')
    
    def validate_phone_number(self, value):
        """Check if phone number already exists"""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered")
        return value
    
    def create(self, validated_data):
        """Create farmer user without password (SMS-based login)"""
        # Set a random unusable password
        import secrets
        random_password = secrets.token_urlsafe(32)
        
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
        
        # Create farmer profile
        FarmerProfile.objects.create(
            user=user,
            farm_size=0,
            primary_crop='maize'
        )
        
        return user


class FarmerSMSLoginRequestSerializer(serializers.Serializer):
    """Request OTP for farmer SMS-based login"""
    
    phone_number = serializers.CharField()
    
    def validate_phone_number(self, value):
        """Validate that phone number exists and is a farmer"""
        try:
            user = User.objects.get(phone_number=value)
            if user.role != 'farmer':
                raise serializers.ValidationError(
                    "SMS login is only available for farmers. Please use password login."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError("Phone number not registered")
        return value


class FarmerSMSLoginVerifySerializer(serializers.Serializer):
    """Verify OTP for farmer SMS-based login"""
    
    phone_number = serializers.CharField()
    otp_code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        if user.role != 'farmer':
            raise serializers.ValidationError("SMS login only available for farmers")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        # Check OTP code
        if user.verification_code != data['otp_code']:
            raise serializers.ValidationError("Invalid OTP code")
        
        # Check if OTP is expired (10 minutes)
        if user.verification_code_created_at:
            time_diff = timezone.now() - user.verification_code_created_at
            if time_diff.total_seconds() > 600:  # 10 minutes
                raise serializers.ValidationError("OTP code has expired")
        
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