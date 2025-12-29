"""
Custom permissions for Community app
"""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow users to only edit their own content"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
