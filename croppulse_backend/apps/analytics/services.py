"""
Business logic services for Analytics app
"""
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from typing import Dict, List
from apps.users.models import User
from apps.weather.models import WeatherData
from apps.observations.models import FarmObservation, PestDiseaseReport
from apps.alerts.models import Alert
from apps.community.models import ForumPost, DirectMessage
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service class for analytics operations"""
    
    @staticmethod
    def get_user_statistics(county: str = None) -> Dict:
        """
        Get user statistics
        
        Args:
            county: Optional county filter
            
        Returns:
            dict: User statistics
        """
        query = Q()
        if county:
            query = Q(county__iexact=county)
        
        users = User.objects.filter(query)
        
        total_users = users.count()
        by_role = users.values('role').annotate(count=Count('id'))
        verified_count = users.filter(is_verified=True).count()
        active_count = users.filter(is_active=True).count()
        
        # Users registered in last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        new_users = users.filter(created_at__gte=thirty_days_ago).count()
        
        return {
            'total_users': total_users,
            'verified_users': verified_count,
            'active_users': active_count,
            'new_users_30_days': new_users,
            'by_role': list(by_role),
            'county': county
        }
    
    @staticmethod
    def get_weather_statistics(county: str = None, days: int = 30) -> Dict:
        """
        Get weather statistics
        
        Args:
            county: Optional county filter
            days: Number of days to analyze
            
        Returns:
            dict: Weather statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        query = Q(recorded_at__gte=start_date)
        if county:
            query &= Q(county__iexact=county)
        
        weather_data = WeatherData.objects.filter(query)
        
        if not weather_data.exists():
            return {}
        
        aggregates = weather_data.aggregate(
            avg_temp=Avg('temperature'),
            avg_humidity=Avg('humidity'),
            total_rainfall=Avg('rainfall'),
            count=Count('id')
        )
        
        return {
            'period_days': days,
            'data_points': aggregates['count'],
            'average_temperature': round(aggregates['avg_temp'] or 0, 2),
            'average_humidity': round(aggregates['avg_humidity'] or 0, 2),
            'average_rainfall': round(aggregates['total_rainfall'] or 0, 2),
            'county': county
        }
    
    @staticmethod
    def get_observation_statistics(county: str = None, days: int = 30) -> Dict:
        """
        Get observation statistics
        
        Args:
            county: Optional county filter
            days: Number of days to analyze
            
        Returns:
            dict: Observation statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        query = Q(created_at__gte=start_date)
        if county:
            query &= Q(county__iexact=county)
        
        observations = FarmObservation.objects.filter(query)
        
        total = observations.count()
        by_type = observations.values('observation_type').annotate(count=Count('id'))
        by_status = observations.values('status').annotate(count=Count('id'))
        
        avg_quality = observations.filter(
            quality_score__gt=0
        ).aggregate(avg=Avg('quality_score'))
        
        return {
            'period_days': days,
            'total_observations': total,
            'by_type': list(by_type),
            'by_status': list(by_status),
            'average_quality_score': round(avg_quality['avg'] or 0, 2),
            'county': county
        }
    
    @staticmethod
    def get_pest_disease_statistics(county: str = None, days: int = 30) -> Dict:
        """
        Get pest and disease statistics
        
        Args:
            county: Optional county filter
            days: Number of days to analyze
            
        Returns:
            dict: Pest/disease statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        query = Q(created_at__gte=start_date)
        if county:
            query &= Q(county__iexact=county)
        
        reports = PestDiseaseReport.objects.filter(query)
        
        total = reports.count()
        by_type = reports.values('pest_or_disease').annotate(count=Count('id'))
        by_severity = reports.values('severity').annotate(count=Count('id'))
        unresolved = reports.filter(is_resolved=False).count()
        
        # Top pests/diseases
        top_issues = (
            reports.values('name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        
        return {
            'period_days': days,
            'total_reports': total,
            'unresolved_reports': unresolved,
            'by_type': list(by_type),
            'by_severity': list(by_severity),
            'top_issues': list(top_issues),
            'county': county
        }
    
    @staticmethod
    def get_alert_statistics(county: str = None, days: int = 30) -> Dict:
        """
        Get alert statistics
        
        Args:
            county: Optional county filter
            days: Number of days to analyze
            
        Returns:
            dict: Alert statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        query = Q(created_at__gte=start_date)
        if county:
            query &= Q(counties__contains=[county])
        
        alerts = Alert.objects.filter(query)
        
        total = alerts.count()
        active = alerts.filter(status='active').count()
        by_type = alerts.values('alert_type').annotate(count=Count('id'))
        by_severity = alerts.values('severity').annotate(count=Count('id'))
        
        total_recipients = alerts.aggregate(total=Count('recipients_count'))
        
        return {
            'period_days': days,
            'total_alerts': total,
            'active_alerts': active,
            'by_type': list(by_type),
            'by_severity': list(by_severity),
            'total_recipients': total_recipients['total'] or 0,
            'county': county
        }
    
    @staticmethod
    def get_community_statistics(days: int = 30) -> Dict:
        """
        Get community engagement statistics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            dict: Community statistics
        """
        start_date = timezone.now() - timedelta(days=days)
        
        total_posts = ForumPost.objects.filter(created_at__gte=start_date).count()
        total_messages = DirectMessage.objects.filter(created_at__gte=start_date).count()
        
        # Active users
        active_users = ForumPost.objects.filter(
            created_at__gte=start_date
        ).values('author').distinct().count()
        
        return {
            'period_days': days,
            'total_posts': total_posts,
            'total_messages': total_messages,
            'active_users': active_users,
        }
    
    @staticmethod
    def get_comprehensive_dashboard(county: str = None, days: int = 30) -> Dict:
        """
        Get comprehensive dashboard data
        
        Args:
            county: Optional county filter
            days: Number of days for trends
            
        Returns:
            dict: Complete dashboard data
        """
        return {
            'users': AnalyticsService.get_user_statistics(county),
            'weather': AnalyticsService.get_weather_statistics(county, days),
            'observations': AnalyticsService.get_observation_statistics(county, days),
            'pest_disease': AnalyticsService.get_pest_disease_statistics(county, days),
            'alerts': AnalyticsService.get_alert_statistics(county, days),
            'community': AnalyticsService.get_community_statistics(days),
            'generated_at': timezone.now().isoformat(),
        }
