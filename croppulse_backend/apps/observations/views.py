"""
Views for Observations app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import FarmObservation, CropReport, PestDiseaseReport
from .serializers import FarmObservationSerializer, CropReportSerializer, PestDiseaseReportSerializer
from .services import ObservationService
from core.permissions import CanVerifyObservations
from core.pagination import StandardResultsSetPagination


class FarmObservationViewSet(viewsets.ModelViewSet):
    """Farm observation management"""
    
    queryset = FarmObservation.objects.all()
    serializer_class = FarmObservationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['observation_type', 'status', 'county']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'quality_score']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_farmer:
            return FarmObservation.objects.filter(user=user)
        elif user.is_field_officer or user.is_hq_analyst:
            return FarmObservation.objects.all()
        return FarmObservation.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[CanVerifyObservations])
    def verify(self, request, pk=None):
        """Verify an observation"""
        observation = self.get_object()
        verification_notes = request.data.get('verification_notes', '')
        
        observation.status = 'verified'
        observation.verified_by = request.user
        observation.verified_at = timezone.now()
        observation.verification_notes = verification_notes
        observation.quality_score = ObservationService.calculate_quality_score(observation)
        observation.save()
        
        return Response({'message': 'Observation verified successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[CanVerifyObservations])
    def reject(self, request, pk=None):
        """Reject an observation"""
        observation = self.get_object()
        verification_notes = request.data.get('verification_notes', '')
        
        observation.status = 'rejected'
        observation.verified_by = request.user
        observation.verified_at = timezone.now()
        observation.verification_notes = verification_notes
        observation.save()
        
        return Response({'message': 'Observation rejected'})


class CropReportViewSet(viewsets.ModelViewSet):
    """Crop report management"""
    
    queryset = CropReport.objects.all()
    serializer_class = CropReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['crop_type', 'current_stage', 'health_status']
    ordering_fields = ['created_at', 'planting_date']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_farmer:
            return CropReport.objects.filter(user=user)
        elif user.is_field_officer or user.is_hq_analyst:
            return CropReport.objects.all()
        return CropReport.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PestDiseaseReportViewSet(viewsets.ModelViewSet):
    """Pest and disease report management"""
    
    queryset = PestDiseaseReport.objects.all()
    serializer_class = PestDiseaseReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['pest_or_disease', 'severity', 'county', 'is_resolved']
    ordering_fields = ['created_at', 'severity']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_farmer:
            return PestDiseaseReport.objects.filter(user=user)
        elif user.is_field_officer or user.is_hq_analyst:
            return PestDiseaseReport.objects.all()
        return PestDiseaseReport.objects.none()
    
    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        
        # Notify if severe
        if report.severity in ['high', 'severe'] or report.requires_assistance:
            ObservationService.notify_pest_disease_alert(report)
    
    @action(detail=True, methods=['post'])
    def mark_resolved(self, request, pk=None):
        """Mark pest/disease report as resolved"""
        report = self.get_object()
        
        if request.user != report.user:
            return Response(
                {'error': 'Only the report creator can mark it as resolved'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        report.is_resolved = True
        report.resolved_at = timezone.now()
        report.save()
        
        return Response({'message': 'Report marked as resolved'})
