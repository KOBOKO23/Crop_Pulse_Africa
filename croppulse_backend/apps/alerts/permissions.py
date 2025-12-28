"""
Custom permissions for Alerts app
"""
from rest_framework import permissions


class CanCreateAlert(permissions.BasePermission):
    """Permission to create alerts - HQ Analysts only"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'hq_analyst'
        )
