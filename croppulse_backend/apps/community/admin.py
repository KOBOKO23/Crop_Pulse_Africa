"""
Admin configuration for Community app
"""
from django.contrib import admin
from .models import (
    ForumCategory, ForumPost, ForumReply,
    DirectMessage, KnowledgeArticle, Like
)


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views_count', 'likes_count', 'replies_count', 'is_approved', 'created_at']
    list_filter = ['category', 'is_approved', 'is_pinned', 'created_at']
    search_fields = ['title', 'content', 'author__full_name']
    raw_id_fields = ['author', 'category']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'likes_count', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__full_name']
    raw_id_fields = ['author', 'post', 'parent']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'message', 'sender__full_name', 'recipient__full_name']
    raw_id_fields = ['sender', 'recipient', 'reply_to']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'views_count', 'likes_count', 'is_published', 'published_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'summary', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['-published_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
