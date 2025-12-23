"""
Admin configuration for Users app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FarmerProfile, FieldOfficerProfile, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for User model"""
    
    list_display = ['phone_number', 'full_name', 'role', 'county', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'county', 'created_at']
    search_fields = ['phone_number', 'full_name', 'email', 'county']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'profile_picture')}),
        ('Role & Location', {'fields': ('role', 'county', 'subcounty', 'ward', 'village')}),
        ('Verification', {'fields': ('is_verified', 'verification_code', 'verification_code_created_at')}),
        ('Preferences', {'fields': ('language', 'receive_sms_notifications', 'receive_push_notifications', 'fcm_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    """Admin for Farmer Profile"""
    
    list_display = ['user', 'farm_name', 'farm_size', 'primary_crop', 'farming_type', 'created_at']
    list_filter = ['farming_type', 'has_irrigation', 'has_greenhouse', 'created_at']
    search_fields = ['user__full_name', 'user__phone_number', 'farm_name', 'primary_crop']
    raw_id_fields = ['user']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Farm Details', {'fields': ('farm_name', 'farm_size', 'primary_crop', 'secondary_crops')}),
        ('Location', {'fields': ('latitude', 'longitude')}),
        ('Farming Info', {'fields': ('years_of_experience', 'farming_type', 'has_irrigation', 'has_greenhouse')}),
        ('Additional', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FieldOfficerProfile)
class FieldOfficerProfileAdmin(admin.ModelAdmin):
    """Admin for Field Officer Profile"""
    
    list_display = ['user', 'employee_id', 'supervisor', 'coverage_area_radius', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__full_name', 'user__phone_number', 'employee_id']
    raw_id_fields = ['user', 'supervisor']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Work Details', {'fields': ('employee_id', 'assigned_counties', 'assigned_subcounties')}),
        ('Supervision', {'fields': ('supervisor', 'coverage_area_radius')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for Notifications"""
    
    list_display = ['title', 'user', 'type', 'priority', 'is_read', 'sent_via_push', 'sent_via_sms', 'created_at']
    list_filter = ['type', 'priority', 'is_read', 'sent_via_push', 'sent_via_sms', 'created_at']
    search_fields = ['title', 'message', 'user__full_name', 'user__phone_number']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Notification', {'fields': ('type', 'priority', 'title', 'message', 'data')}),
        ('Status', {'fields': ('is_read', 'read_at')}),
        ('Related Object', {'fields': ('related_object_type', 'related_object_id')}),
        ('Delivery', {'fields': ('sent_via_push', 'sent_via_sms')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    readonly_fields = ['created_at', 'read_at']
