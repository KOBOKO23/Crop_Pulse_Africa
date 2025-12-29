"""
Views for Community app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import models
from .models import (
    ForumCategory, ForumPost, ForumReply,
    DirectMessage, KnowledgeArticle, Like
)
from .serializers import (
    ForumCategorySerializer, ForumPostSerializer, ForumReplySerializer,
    DirectMessageSerializer, KnowledgeArticleSerializer, LikeSerializer
)
from .services import CommunityService
from core.pagination import StandardResultsSetPagination


class ForumCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Forum category listing"""
    
    queryset = ForumCategory.objects.filter(is_active=True)
    serializer_class = ForumCategorySerializer
    permission_classes = [IsAuthenticated]


class ForumPostViewSet(viewsets.ModelViewSet):
    """Forum post management"""
    
    queryset = ForumPost.objects.filter(is_approved=True)
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving a post"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a forum post"""
        post = self.get_object()
        
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type='forum_post',
            object_id=post.id
        )
        
        if created:
            post.likes_count += 1
            post.save(update_fields=['likes_count'])
            message = 'Post liked'
        else:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])
            message = 'Post unliked'
        
        return Response({'message': message, 'liked': created})


class ForumReplyViewSet(viewsets.ModelViewSet):
    """Forum reply management"""
    
    queryset = ForumReply.objects.filter(is_approved=True)
    serializer_class = ForumReplySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def perform_create(self, serializer):
        reply = serializer.save(author=self.request.user)
        
        # Update post reply count
        post = reply.post
        post.replies_count += 1
        post.save(update_fields=['replies_count'])
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a reply"""
        reply = self.get_object()
        
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type='forum_reply',
            object_id=reply.id
        )
        
        if created:
            reply.likes_count += 1
            reply.save(update_fields=['likes_count'])
            message = 'Reply liked'
        else:
            like.delete()
            reply.likes_count = max(0, reply.likes_count - 1)
            reply.save(update_fields=['likes_count'])
            message = 'Reply unliked'
        
        return Response({'message': message, 'liked': created})


class DirectMessageViewSet(viewsets.ModelViewSet):
    """Direct message management"""
    
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Get messages sent or received by the user"""
        user = self.request.user
        return DirectMessage.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        
        if message.recipient != request.user:
            return Response(
                {'error': 'Only the recipient can mark this message as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save(update_fields=['is_read', 'read_at'])
        
        return Response({'message': 'Message marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = DirectMessage.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': count})


class KnowledgeArticleViewSet(viewsets.ModelViewSet):
    """Knowledge article management"""
    
    queryset = KnowledgeArticle.objects.filter(is_published=True)
    serializer_class = KnowledgeArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['category']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['published_at', 'views_count', 'likes_count']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving an article"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like an article"""
        article = self.get_object()
        
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type='knowledge_article',
            object_id=article.id
        )
        
        if created:
            article.likes_count += 1
            article.save(update_fields=['likes_count'])
            message = 'Article liked'
        else:
            like.delete()
            article.likes_count = max(0, article.likes_count - 1)
            article.save(update_fields=['likes_count'])
            message = 'Article unliked'
        
        return Response({'message': message, 'liked': created})
