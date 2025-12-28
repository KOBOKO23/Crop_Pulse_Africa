"""
Serializers for Alerts app
"""
from rest_framework import serializers
from .models import Alert, AlertAcknowledgment, AlertLog


class AlertSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'severity', 'title', 'message', 'description',
            'counties', 'subcounties', 'start_time', 'end_time', 'status',
            'recommendations', 'action_required', 'action_description',
            'created_by', 'created_by_name', 'recipients_count',
            'require_acknowledgment', 'acknowledgment_count',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'recipients_count', 'acknowledgment_count', 'created_at', 'updated_at']
    
    def get_is_active(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.status == 'active' and obj.start_time <= now <= obj.end_time


class AlertAcknowledgmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    alert_title = serializers.CharField(source='alert.title', read_only=True)
    
    class Meta:
        model = AlertAcknowledgment
        fields = ['id', 'alert', 'alert_title', 'user', 'user_name', 'acknowledged_at', 'notes']
        read_only_fields = ['id', 'user', 'acknowledged_at']


class AlertLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = AlertLog
        fields = ['id', 'alert', 'user', 'user_name', 'delivery_method', 'delivered_at', 'was_successful', 'error_message']
        read_only_fields = ['id', 'delivered_at']
