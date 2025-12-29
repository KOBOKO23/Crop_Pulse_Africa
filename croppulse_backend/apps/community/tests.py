"""
Tests for Community app
"""
from django.test import TestCase
from apps.users.models import User
from .models import ForumCategory, ForumPost, ForumReply


class CommunityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+254712345678',
            password='testpass123',
            full_name='Test Farmer',
            role='farmer'
        )
        
        self.category = ForumCategory.objects.create(
            name='Crop Management',
            description='Discuss crop management techniques'
        )
    
    def test_create_forum_post(self):
        post = ForumPost.objects.create(
            category=self.category,
            author=self.user,
            title='Best practices for maize farming',
            content='What are the best practices for maize farming in Kenya?'
        )
        
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)
        self.assertTrue(post.is_approved)
