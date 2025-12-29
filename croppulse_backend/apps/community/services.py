"""
Business logic services for Community app
"""
from django.db.models import Count, Q
from typing import Dict, List
from .models import ForumPost, ForumReply, KnowledgeArticle, DirectMessage
import logging

logger = logging.getLogger(__name__)


class CommunityService:
    """Service class for community-related operations"""
    
    @staticmethod
    def get_trending_posts(limit: int = 10) -> List[ForumPost]:
        """
        Get trending forum posts based on recent engagement
        
        Args:
            limit: Number of posts to return
            
        Returns:
            list: ForumPost instances
        """
        from datetime import timedelta
        from django.utils import timezone
        
        week_ago = timezone.now() - timedelta(days=7)
        
        posts = (
            ForumPost.objects
            .filter(is_approved=True, created_at__gte=week_ago)
            .order_by('-likes_count', '-replies_count', '-views_count')
            [:limit]
        )
        
        return list(posts)
    
    @staticmethod
    def get_community_statistics() -> Dict:
        """
        Get community engagement statistics
        
        Returns:
            dict: Statistics
        """
        total_posts = ForumPost.objects.filter(is_approved=True).count()
        total_replies = ForumReply.objects.filter(is_approved=True).count()
        total_articles = KnowledgeArticle.objects.filter(is_published=True).count()
        
        # Active users (posted in last 30 days)
        from datetime import timedelta
        from django.utils import timezone
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        active_users = ForumPost.objects.filter(
            created_at__gte=thirty_days_ago
        ).values('author').distinct().count()
        
        return {
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_articles': total_articles,
            'active_users': active_users,
        }
