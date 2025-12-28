"""
Business logic services for Observations app
"""
from django.db.models import Q, Count
from typing import Dict, List
from .models import FarmObservation, CropReport, PestDiseaseReport
from apps.users.models import User
from apps.users.services import UserService
import logging

logger = logging.getLogger(__name__)


class ObservationService:
    """Service class for observation-related operations"""
    
    @staticmethod
    def calculate_quality_score(observation: FarmObservation) -> int:
        """
        Calculate quality score for an observation
        
        Args:
            observation: FarmObservation instance
            
        Returns:
            int: Quality score (0-100)
        """
        score = 0
        
        # Has description (20 points)
        if observation.description and len(observation.description) > 50:
            score += 20
        
        # Has images (30 points total, 10 each)
        if observation.image1:
            score += 10
        if observation.image2:
            score += 10
        if observation.image3:
            score += 10
        
        # Has location (15 points)
        if observation.latitude and observation.longitude:
            score += 15
        
        # Has weather data (15 points)
        if observation.temperature or observation.rainfall:
            score += 15
        
        # Is verified (20 points)
        if observation.status == 'verified':
            score += 20
        
        return min(score, 100)
    
    @staticmethod
    def notify_pest_disease_alert(report: PestDiseaseReport):
        """
        Send notifications for severe pest/disease reports
        
        Args:
            report: PestDiseaseReport instance
        """
        # Get field officers and HQ analysts in the area
        users = User.objects.filter(
            Q(role='field_officer') | Q(role='hq_analyst'),
            county=report.county,
            is_active=True
        )
        
        title = f'Pest/Disease Alert: {report.name}'
        message = (
            f'{report.pest_or_disease.capitalize()} outbreak reported on {report.affected_crop}. '
            f'Severity: {report.severity}. Location: {report.county}. '
            f'Affected area: {report.affected_area}ha.'
        )
        
        UserService.bulk_create_notifications(
            users=list(users),
            notification_type='alert',
            title=title,
            message=message,
            priority='high',
            data={
                'report_id': report.id,
                'pest_or_disease': report.pest_or_disease,
                'severity': report.severity
            },
            send_push=True,
            send_sms=report.severity == 'severe'
        )
        
        logger.info(f'Sent pest/disease alert notifications to {users.count()} users')
    
    @staticmethod
    def get_observation_statistics(county: str = None) -> Dict:
        """
        Get statistics about observations
        
        Args:
            county: Optional county filter
            
        Returns:
            dict: Statistics
        """
        query = Q()
        if county:
            query = Q(county__iexact=county)
        
        observations = FarmObservation.objects.filter(query)
        
        stats = observations.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            verified=Count('id', filter=Q(status='verified')),
            rejected=Count('id', filter=Q(status='rejected'))
        )
        
        type_breakdown = observations.values('observation_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {
            'total_observations': stats['total'],
            'pending': stats['pending'],
            'verified': stats['verified'],
            'rejected': stats['rejected'],
            'by_type': list(type_breakdown),
            'county': county
        }
    
    @staticmethod
    def get_pest_disease_hotspots() -> List[Dict]:
        """
        Identify pest/disease hotspots based on reports
        
        Returns:
            list: Hotspot data by county
        """
        hotspots = (
            PestDiseaseReport.objects
            .filter(is_resolved=False)
            .values('county', 'name', 'pest_or_disease')
            .annotate(count=Count('id'))
            .filter(count__gte=3)  # At least 3 reports
            .order_by('-count')[:10]
        )
        
        return list(hotspots)
