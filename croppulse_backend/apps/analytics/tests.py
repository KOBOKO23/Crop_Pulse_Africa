"""
Tests for Analytics app
"""
from django.test import TestCase
from apps.users.models import User
from .services import AnalyticsService


class AnalyticsTests(TestCase):
    def setUp(self):
        # Create test users
        User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test Farmer',
            role='farmer',
            county='Nairobi'
        )
        
        User.objects.create_user(
            phone_number='+254712345679',
            password='testpass123',
            full_name='Test Officer',
            role='field_officer',
            county='Nairobi'
        )
    
    def test_user_statistics(self):
        stats = AnalyticsService.get_user_statistics('Nairobi')
        
        self.assertEqual(stats['total_users'], 2)
        self.assertEqual(stats['county'], 'Nairobi')
        self.assertIn('by_role', stats)
