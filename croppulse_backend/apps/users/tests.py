"""
Tests for Users app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import FarmerProfile, FieldOfficerProfile, Notification

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for User model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test User',
            role='farmer'
        )
        
        self.assertEqual(user.phone_number, '+254712345678')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.role, 'farmer')
        self.assertFalse(user.is_verified)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            phone_number='+254712345679',
            password='adminpass123',
            full_name='Admin User'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_verified)
        self.assertEqual(user.role, 'hq_analyst')


class AuthenticationTests(APITestCase):
    """Tests for authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/users/auth/register/'
        self.login_url = '/api/v1/users/auth/login/'
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'phone_number': '+254712345678',
            'full_name': 'Test Farmer',
            'role': 'farmer',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'county': 'Nairobi',
            'language': 'en'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['phone_number'], '+254712345678')
        
        # Check that user was created in database
        self.assertTrue(User.objects.filter(phone_number='+254712345678').exists())
    
    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test User',
            role='farmer'
        )
        user.is_verified = True
        user.save()
        
        data = {
            'phone_number': '+254712345678',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
