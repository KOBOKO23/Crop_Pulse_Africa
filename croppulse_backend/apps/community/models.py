"""
Community models for CropPulse Africa
"""
from django.db import models
from django.conf import settings
from core.utils import get_upload_path

# Named functions for upload_to
def forum_image_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'forum')

def message_attachment_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'messages')

def knowledge_article_upload_to(instance, filename):
    return get_upload_path(instance, filename, 'knowledge')


class ForumCategory(models.Model):
    """Categories for forum discussions"""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'forum_categories'
        verbose_name = 'Forum Category'
        verbose_name_plural = 'Forum Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ForumPost(models.Model):
    """Community forum posts"""
    
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Media
    image = models.ImageField(
        upload_to=forum_image_upload_to,
        blank=True,
        null=True
    )
    
    # Tags
    tags = models.JSONField(default=list, blank=True)
    
    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    replies_count = models.IntegerField(default=0)
    
    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'forum_posts'
        verbose_name = 'Forum Post'
        verbose_name_plural = 'Forum Posts'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return self.title


class ForumReply(models.Model):
    """Replies to forum posts"""
    
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.TextField()
    
    # Parent reply (for nested replies)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_replies'
    )
    
    # Engagement
    likes_count = models.IntegerField(default=0)
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'forum_replies'
        verbose_name = 'Forum Reply'
        verbose_name_plural = 'Forum Replies'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply by {self.author.full_name} on {self.post.title}"


class DirectMessage(models.Model):
    """Direct messages between users"""
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    
    # Attachments
    attachment = models.FileField(
        upload_to=message_attachment_upload_to,
        blank=True,
        null=True
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    # Threading
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'direct_messages'
        verbose_name = 'Direct Message'
        verbose_name_plural = 'Direct Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.full_name} to {self.recipient.full_name}"


class KnowledgeArticle(models.Model):
    """Knowledge base articles"""
    
    ARTICLE_CATEGORIES = [
        ('farming', 'Farming Techniques'),
        ('weather', 'Weather & Climate'),
        ('pests', 'Pest Management'),
        ('diseases', 'Disease Control'),
        ('soil', 'Soil Management'),
        ('irrigation', 'Irrigation'),
        ('harvest', 'Harvesting & Storage'),
        ('market', 'Market Information'),
        ('general', 'General'),
    ]
    
    category = models.CharField(max_length=20, choices=ARTICLE_CATEGORIES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='knowledge_articles'
    )
    
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    
    # Media
    featured_image = models.ImageField(
        upload_to=knowledge_article_upload_to,
        blank=True,
        null=True
    )
    
    # SEO
    tags = models.JSONField(default=list, blank=True)
    
    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    # Publishing
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'knowledge_articles'
        verbose_name = 'Knowledge Article'
        verbose_name_plural = 'Knowledge Articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['category', '-published_at']),
        ]
    
    def __str__(self):
        return self.title


class Like(models.Model):
    """User likes for posts, replies, and articles"""
    
    CONTENT_TYPES = [
        ('forum_post', 'Forum Post'),
        ('forum_reply', 'Forum Reply'),
        ('knowledge_article', 'Knowledge Article'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = [['user', 'content_type', 'object_id']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} liked {self.content_type} #{self.object_id}"
