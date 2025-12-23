"""
URL patterns for Users app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, UserViewSet, NotificationViewSet,
    FarmerProfileViewSet, FieldOfficerProfileViewSet,
    FarmerAuthViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'farmer-auth', FarmerAuthViewSet, basename='farmer-auth')
router.register(r'users', UserViewSet, basename='user')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'farmer-profiles', FarmerProfileViewSet, basename='farmer-profile')
router.register(r'field-officer-profiles', FieldOfficerProfileViewSet, basename='field-officer-profile')

urlpatterns = [
    path('', include(router.urls)),
]