"""
Views for Users app
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import User, Notification, FarmerProfile, FieldOfficerProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    VerifyPhoneSerializer, ResendVerificationSerializer,
    NotificationSerializer, UpdateProfileSerializer,
    ChangePasswordSerializer, UpdateFCMTokenSerializer,
    FarmerProfileSerializer, FieldOfficerProfileSerializer,
    FarmerSimpleRegistrationSerializer, FarmerSMSLoginRequestSerializer,
    FarmerSMSLoginVerifySerializer, OnboardingStatusSerializer
)
from .services import UserService
from core.pagination import StandardResultsSetPagination, NotificationPagination


class AuthViewSet(viewsets.GenericViewSet):
    """Authentication endpoints"""
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification code via SMS
        UserService.send_verification_code(user)
        
        return Response({
            'message': 'Registration successful. Verification code sent via SMS.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login user"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def verify_phone(self, request):
        """Verify phone number"""
        serializer = VerifyPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Mark as verified
        user.is_verified = True
        user.verification_code = ''
        user.save(update_fields=['is_verified', 'verification_code'])
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Phone number verified successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """Resend verification code"""
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
            
            if user.is_verified:
                return Response(
                    {'message': 'Phone number already verified'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            UserService.send_verification_code(user)
            
            return Response({'message': 'Verification code sent'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({'message': 'Logout successful'})
        except Exception:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Filter users based on role"""
        user = self.request.user
        
        if user.is_hq_analyst:
            return User.objects.all()
        elif user.is_field_officer:
            # Field officers can see farmers in their area
            return User.objects.filter(role='farmer')
        else:
            # Farmers can only see their own profile
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update user profile"""
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})
    
    @action(detail=False, methods=['post'])
    def update_fcm_token(self, request):
        """Update FCM token for push notifications"""
        serializer = UpdateFCMTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request.user.fcm_token = serializer.validated_data['fcm_token']
        request.user.save(update_fields=['fcm_token'])
        
        return Response({'message': 'FCM token updated'})


class FarmerProfileViewSet(viewsets.ModelViewSet):
    """Farmer profile management"""
    
    queryset = FarmerProfile.objects.all()
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
    """Field officer profile management"""
    
    queryset = FieldOfficerProfile.objects.all()
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
    """User notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """List notifications with unread count"""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Add unread count to paginator
            self.paginator.unread_count = queryset.filter(is_read=False).count()
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return Response({'message': f'{updated} notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count"""
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': count})


# Farmer-specific simplified authentication
class FarmerAuthViewSet(viewsets.GenericViewSet):
    """Simplified authentication for farmers"""
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Simplified farmer registration - minimal fields, no password"""
        serializer = FarmerSimpleRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send OTP via SMS
        UserService.send_login_otp(user)
        
        return Response({
            'message': 'Registration successful. Login code sent via SMS.',
            'phone_number': str(user.phone_number),
            'requires_verification': True
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        """Request OTP for SMS-based login"""
        serializer = FarmerSMSLoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
        
        # Send OTP
        UserService.send_login_otp(user)
        
        return Response({
            'message': 'Login code sent via SMS',
            'phone_number': str(user.phone_number)
        })
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """Verify OTP and login"""
        serializer = FarmerSMSLoginVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Clear the OTP after successful login
        user.verification_code = ''
        user.save(update_fields=['verification_code'])
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Get onboarding status
        onboarding = UserService.get_onboarding_status(user)
        
        # Get simplified dashboard data
        dashboard_data = UserService.get_farmer_dashboard_data(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'phone_number': str(user.phone_number),
                'full_name': user.full_name,
                'county': user.county,
                'language': user.language,
                'is_verified': user.is_verified,
            },
            'onboarding': onboarding,
            'dashboard': dashboard_data
        })


class DashboardViewSet(viewsets.GenericViewSet):
    """Role-specific dashboard data"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def farmer(self, request):
        """Get farmer dashboard data"""
        if not request.user.is_farmer:
            return Response(
                {'error': 'This endpoint is only for farmers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = UserService.get_farmer_dashboard_data(request.user)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def field_officer(self, request):
        """Get field officer dashboard data"""
        if not request.user.is_field_officer:
            return Response(
                {'error': 'This endpoint is only for field officers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = UserService.get_field_officer_dashboard_data(request.user)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def onboarding_status(self, request):
        """Get user's onboarding status"""
        status_data = UserService.get_onboarding_status(request.user)
        serializer = OnboardingStatusSerializer(status_data)
        return Response(serializer.data)