"""
URL patterns for Community app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ForumCategoryViewSet, ForumPostViewSet, ForumReplyViewSet,
    DirectMessageViewSet, KnowledgeArticleViewSet
)

router = DefaultRouter()
router.register(r'forum-categories', ForumCategoryViewSet, basename='forum-category')
router.register(r'forum-posts', ForumPostViewSet, basename='forum-post')
router.register(r'forum-replies', ForumReplyViewSet, basename='forum-reply')
router.register(r'messages', DirectMessageViewSet, basename='message')
router.register(r'knowledge-articles', KnowledgeArticleViewSet, basename='knowledge-article')

urlpatterns = [
    path('', include(router.urls)),
]
