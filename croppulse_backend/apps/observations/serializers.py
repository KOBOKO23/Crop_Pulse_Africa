"""
Serializers for Observations app
"""
from rest_framework import serializers
from .models import FarmObservation, CropReport, PestDiseaseReport


class FarmObservationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.full_name', read_only=True)
    
    class Meta:
        model = FarmObservation
        fields = [
            'id', 'user', 'user_name', 'observation_type', 'title', 'description',
            'latitude', 'longitude', 'county', 'location_description',
            'image1', 'image2', 'image3', 'audio_note', 'temperature', 'rainfall',
            'status', 'verified_by', 'verified_by_name', 'verified_at',
            'verification_notes', 'quality_score', 'is_public', 'views_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'verified_by', 'verified_at', 'quality_score', 'views_count', 'created_at', 'updated_at']


class CropReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = CropReport
        fields = [
            'id', 'user', 'user_name', 'crop_type', 'variety', 'area_planted',
            'planting_date', 'current_stage', 'health_status', 'notes',
            'challenges', 'crop_image', 'expected_harvest_date', 'expected_yield',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PestDiseaseReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = PestDiseaseReport
        fields = [
            'id', 'user', 'user_name', 'name', 'pest_or_disease', 'affected_crop',
            'severity', 'symptoms', 'affected_area', 'latitude', 'longitude',
            'county', 'image1', 'image2', 'control_measures_taken',
            'requires_assistance', 'is_resolved', 'resolved_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'resolved_at', 'created_at', 'updated_at']
