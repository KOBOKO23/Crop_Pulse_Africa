"""
Custom permissions for Users app
"""
from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """Allow users to only access their own profile"""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanManageUsers(permissions.BasePermission):
    """Permission to manage users - HQ Analysts only"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'hq_analyst'
        )
