"""
Admin configuration for Observations app
"""
from django.contrib import admin
from .models import FarmObservation, CropReport, PestDiseaseReport


@admin.register(FarmObservation)
class FarmObservationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'observation_type', 'county', 'status', 'quality_score', 'created_at']
    list_filter = ['observation_type', 'status', 'county', 'created_at']
    search_fields = ['title', 'description', 'user__full_name']
    raw_id_fields = ['user', 'verified_by']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(CropReport)
class CropReportAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'user', 'current_stage', 'health_status', 'planting_date', 'created_at']
    list_filter = ['crop_type', 'current_stage', 'health_status', 'created_at']
    search_fields = ['crop_type', 'variety', 'user__full_name']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(PestDiseaseReport)
class PestDiseaseReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'pest_or_disease', 'affected_crop', 'severity', 'county', 'is_resolved', 'created_at']
    list_filter = ['pest_or_disease', 'severity', 'county', 'is_resolved', 'created_at']
    search_fields = ['name', 'affected_crop', 'symptoms', 'user__full_name']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
