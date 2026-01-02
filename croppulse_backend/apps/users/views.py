"""
Views for Users app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db import IntegrityError, transaction
from .models import User, Notification, FarmerProfile, FieldOfficerProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    VerifyPhoneSerializer, ResendVerificationSerializer,
    NotificationSerializer, UpdateProfileSerializer,
    ChangePasswordSerializer, UpdateFCMTokenSerializer,
    FarmerProfileSerializer, FieldOfficerProfileSerializer,
    FarmerSimpleRegistrationSerializer, FarmerSMSLoginRequestSerializer,
    FarmerSMSLoginVerifySerializer, OnboardingStatusSerializer,
    AuthActionSerializer
)
from .services import UserService
from core.pagination import StandardResultsSetPagination, NotificationPagination


class AuthViewSet(viewsets.GenericViewSet):
    """Authentication endpoints"""

    permission_classes = [AllowAny]
    serializer_class = AuthActionSerializer  # default for OPTIONS

    def get_serializer_class(self):
        """Map actions to serializers"""
        mapping = {
            'register': UserRegistrationSerializer,
            'login': UserLoginSerializer,
            'verify_phone': VerifyPhoneSerializer,
            'resend_verification': ResendVerificationSerializer,
        }
        return mapping.get(self.action, AuthActionSerializer)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = serializer.save()
        except IntegrityError:
            return Response({'error': 'User with this phone number or email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        UserService.send_verification_code(user)

        return Response({
            'message': 'Registration successful. Verification code sent via SMS.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'])
    def verify_phone(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.is_verified = True
        user.verification_code = ''
        user.save(update_fields=['is_verified', 'verification_code'])

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Phone number verified successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone_number']
        try:
            user = User.objects.get(phone_number=phone)
            if user.is_verified:
                return Response({'message': 'Phone number already verified'},
                                status=status.HTTP_400_BAD_REQUEST)
            UserService.send_verification_code(user)
            return Response({'message': 'Verification code sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Logout successful'})
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """User management"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_hq_analyst:
            return User.objects.all()
        elif user.is_field_officer:
            return User.objects.filter(role='farmer')
        else:
            return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = UpdateProfileSerializer(
            request.user, data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'})

    @action(detail=False, methods=['post'])
    def update_fcm_token(self, request):
        serializer = UpdateFCMTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.fcm_token = serializer.validated_data['fcm_token']
        request.user.save(update_fields=['fcm_token'])
        return Response({'message': 'FCM token updated'})


class FarmerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_farmer:
            return FarmerProfile.objects.filter(user=user)
        elif user.is_field_officer or user.is_hq_analyst:
            return FarmerProfile.objects.all()
        return FarmerProfile.objects.none()


class FieldOfficerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = FieldOfficerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_field_officer:
            return FieldOfficerProfile.objects.filter(user=user)
        elif user.is_hq_analyst:
            return FieldOfficerProfile.objects.all()
        return FieldOfficerProfile.objects.none()


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.mark_as_read()
        return Response({'message': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        updated = Notification.objects.filter(
            user=request.user, is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'message': f'{updated} notifications marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class FarmerAuthViewSet(viewsets.GenericViewSet):
    """Simplified SMS login for farmers"""

    permission_classes = [AllowAny]
    serializer_class = AuthActionSerializer

    def get_serializer_class(self):
        mapping = {
            'register': FarmerSimpleRegistrationSerializer,
            'request_otp': FarmerSMSLoginRequestSerializer,
            'verify_otp': FarmerSMSLoginVerifySerializer,
        }
        return mapping.get(self.action, AuthActionSerializer)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register farmer and send OTP"""
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 70)
        logger.info("📝 FARMER REGISTRATION")
        logger.info("=" * 70)
        logger.info(f"Data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"❌ Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        
        # Check if already exists
        if User.objects.filter(phone_number=phone).exists():
            logger.error(f"❌ Phone already registered: {phone}")
            return Response(
                {'error': 'Phone number already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create user
            with transaction.atomic():
                user = serializer.save()
                logger.info(f"✅ User created: {user.full_name}")
            
            # Send OTP
            logger.info("📤 Sending OTP...")
            success = UserService.send_login_otp(user)
            
            # Reload user to get updated OTP
            user.refresh_from_db()
            
            logger.info(f"OTP: {user.verification_code}")
            logger.info(f"SMS sent: {success}")
            logger.info("=" * 70)
            
            return Response({
                'message': 'Registration successful. OTP sent via SMS.',
                'phone_number': str(user.phone_number),
                'requires_verification': True
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"❌ Registration failed: {str(e)}")
            logger.exception(e)
            return Response(
                {'error': 'Registration failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
        UserService.send_login_otp(user)
        return Response({'message': 'Login code sent via SMS', 'phone_number': str(user.phone_number)})

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """Verify OTP and login"""
        import logging
        logger = logging.getLogger(__name__)
        
        # Log request
        logger.info("=" * 70)
        logger.info("📥 VERIFY OTP REQUEST")
        logger.info("=" * 70)
        logger.info(f"Data: {request.data}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Validate with serializer
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error("❌ Validation failed")
            logger.error(f"Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated user
        user = serializer.validated_data['user']
        logger.info(f"✅ User validated: {user.full_name}")
        
        # Update user
        user.last_login = timezone.now()
        user.is_active = True
        user.is_verified = True
        user.verification_code = None
        user.verification_code_created_at = None
        user.save()
        
        logger.info("✅ User updated and activated")
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Get additional data
        try:
            onboarding = UserService.get_onboarding_status(user)
            dashboard = UserService.get_farmer_dashboard_data(user)
        except Exception as e:
            logger.warning(f"⚠️ Could not load dashboard data: {e}")
            onboarding = {}
            dashboard = {}
        
        logger.info("✅ Login successful")
        logger.info("=" * 70)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'phone_number': str(user.phone_number),
                'full_name': user.full_name,
                'county': user.county,
                'language': user.language,
                'role': user.role,
                'is_verified': user.is_verified,
            },
            'onboarding': onboarding,
            'dashboard': dashboard
        }, status=status.HTTP_200_OK)


class DashboardViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def farmer(self, request):
        if not request.user.is_farmer:
            return Response({'error': 'Only for farmers'}, status=status.HTTP_403_FORBIDDEN)
        data = UserService.get_farmer_dashboard_data(request.user)
        return Response(data)

    @action(detail=False, methods=['get'])
    def field_officer(self, request):
        if not request.user.is_field_officer:
            return Response({'error': 'Only for field officers'}, status=status.HTTP_403_FORBIDDEN)
        data = UserService.get_field_officer_dashboard_data(request.user)
        return Response(data)

    @action(detail=False, methods=['get'])
    def onboarding_status(self, request):
        status_data = UserService.get_onboarding_status(request.user)
        serializer = OnboardingStatusSerializer(status_data)
        return Response(serializer.data)
    

"""
Add this to apps/users/views.py for debugging
REMOVE THIS IN PRODUCTION!
"""
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def debug_otp(request):
    """
    Debug endpoint to check OTP status
    
    GET /api/v1/users/debug-otp/?phone=+254712345678
    POST /api/v1/users/debug-otp/ with {"phone_number": "+254712345678"}
    
    IMPORTANT: Only works in DEBUG mode. Remove in production!
    """
    if not settings.DEBUG:
        return Response(
            {"error": "This endpoint is only available in DEBUG mode"},
            status=403
        )
    
    # Get phone number from query params or body
    if request.method == 'GET':
        phone = request.query_params.get('phone')
    else:
        phone = request.data.get('phone_number')
    
    if not phone:
        return Response({"error": "phone or phone_number required"}, status=400)
    
    try:
        user = User.objects.get(phone_number=phone)
        
        # Calculate OTP age if exists
        otp_age_seconds = None
        otp_expired = None
        if user.verification_code_created_at:
            elapsed = timezone.now() - user.verification_code_created_at
            otp_age_seconds = elapsed.total_seconds()
            otp_expired = otp_age_seconds > 600
        
        response_data = {
            "user_id": user.id,
            "phone_number": str(user.phone_number),
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "otp": {
                "code": user.verification_code or None,
                "created_at": user.verification_code_created_at.isoformat() if user.verification_code_created_at else None,
                "age_seconds": otp_age_seconds,
                "expired": otp_expired,
            },
            "has_farmer_profile": hasattr(user, 'farmer_profile'),
        }
        
        logger.info(f"🔍 DEBUG OTP CHECK: {phone} - OTP: {user.verification_code}")
        
        return Response(response_data)
        
    except User.DoesNotExist:
        return Response(
            {"error": f"User not found with phone: {phone}"},
            status=404
        )


# Add this to your urls.py:
# path('debug-otp/', debug_otp, name='debug-otp'),



