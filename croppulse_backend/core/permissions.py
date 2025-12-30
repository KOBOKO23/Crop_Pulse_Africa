"""
Custom permission classes for CropPulse Africa
"""
from rest_framework import permissions


class IsFarmer(permissions.BasePermission):
    """Allow access only to users with Farmer role"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'farmer'
        )


class IsFieldOfficer(permissions.BasePermission):
    """Allow access only to users with Field Officer role"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'field_officer'
        )


class IsHQAnalyst(permissions.BasePermission):
    """Allow access only to users with HQ Analyst role"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'hq_analyst'
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` or `user` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsFarmerOrFieldOfficer(permissions.BasePermission):
    """Allow access to Farmers and Field Officers"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['farmer', 'field_officer']
        )


class IsFieldOfficerOrHQAnalyst(permissions.BasePermission):
    """Allow access to Field Officers and HQ Analysts"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['field_officer', 'hq_analyst']
        )


class CanManageAlerts(permissions.BasePermission):
    """Permission to manage alerts - HQ Analysts only"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'hq_analyst'
        )


class CanVerifyObservations(permissions.BasePermission):
    """Permission to verify observations - Field Officers and HQ Analysts"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['field_officer', 'hq_analyst']
        )


class CanAccessAnalytics(permissions.BasePermission):
    """Permission to access analytics - Field Officers and HQ Analysts"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['field_officer', 'hq_analyst']
        )


class IsVerified(permissions.BasePermission):
    """Allow access only to verified users"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_verified', False)
        )


class CanModerateContent(permissions.BasePermission):
    """Permission to moderate community content"""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.role in ['field_officer', 'hq_analyst'] or 
             getattr(request.user, 'is_moderator', False))
        )
