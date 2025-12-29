"""
Serializers for Community app
"""
from rest_framework import serializers
from .models import (
    ForumCategory, ForumPost, ForumReply,
    DirectMessage, KnowledgeArticle, Like
)


class ForumCategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumCategory
        fields = ['id', 'name', 'description', 'icon', 'order', 'is_active', 'posts_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(is_approved=True).count()


class ForumReplySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = ForumReply
        fields = [
            'id', 'post', 'author', 'author_name', 'content', 'parent',
            'likes_count', 'is_approved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'created_at', 'updated_at']


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    replies = ForumReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = ForumPost
        fields = [
            'id', 'category', 'category_name', 'author', 'author_name',
            'title', 'content', 'image', 'tags', 'views_count',
            'likes_count', 'replies_count', 'is_pinned', 'is_locked',
            'is_approved', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count', 'replies_count',
            'created_at', 'updated_at'
        ]


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    
    class Meta:
        model = DirectMessage
        fields = [
            'id', 'sender', 'sender_name', 'recipient', 'recipient_name',
            'subject', 'message', 'attachment', 'is_read', 'read_at',
            'reply_to', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'read_at', 'created_at']


class KnowledgeArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = KnowledgeArticle
        fields = [
            'id', 'category', 'author', 'author_name', 'title', 'summary',
            'content', 'featured_image', 'tags', 'views_count', 'likes_count',
            'is_published', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'likes_count', 'published_at',
            'created_at', 'updated_at'
        ]


class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_name', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
