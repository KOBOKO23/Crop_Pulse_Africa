"""
Custom permissions for Observations app
"""
from rest_framework import permissions


class IsObservationOwner(permissions.BasePermission):
    """Allow users to only modify their own observations"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
