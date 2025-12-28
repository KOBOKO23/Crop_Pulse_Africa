"""
Tests for Observations app
"""
from django.test import TestCase
from django.utils import timezone
from apps.users.models import User
from .models import FarmObservation, CropReport, PestDiseaseReport


class FarmObservationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test Farmer',
            role='farmer'
        )
    
    def test_create_observation(self):
        observation = FarmObservation.objects.create(
            user=self.user,
            observation_type='weather',
            title='Heavy Rain Observed',
            description='Intense rainfall in the morning',
            latitude=-1.2921,
            longitude=36.8219,
            county='Nairobi',
            rainfall=45.5
        )
        
        self.assertEqual(observation.status, 'pending')
        self.assertEqual(observation.observation_type, 'weather')
