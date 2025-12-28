"""
Tests for Alerts app
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from .models import Alert, AlertAcknowledgment


class AlertTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test User',
            role='hq_analyst'
        )
    
    def test_create_alert(self):
        alert = Alert.objects.create(
            alert_type='weather',
            severity='high',
            title='Heavy Rain Warning',
            message='Expect heavy rainfall in the next 24 hours',
            counties=['Nairobi', 'Kiambu'],
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(days=1),
            status='active',
            created_by=self.user
        )
        
        self.assertEqual(alert.alert_type, 'weather')
        self.assertEqual(alert.severity, 'high')
        self.assertEqual(alert.status, 'active')
