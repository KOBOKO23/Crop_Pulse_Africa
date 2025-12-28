"""
Views for Alerts app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Alert, AlertAcknowledgment
from .serializers import AlertSerializer, AlertAcknowledgmentSerializer
from .services import AlertService
from core.permissions import IsHQAnalyst
from core.pagination import StandardResultsSetPagination


class AlertViewSet(viewsets.ModelViewSet):
    """Alert management"""
    
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['alert_type', 'severity', 'status']
    ordering_fields = ['created_at', 'start_time', 'severity']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHQAnalyst()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user's county
        if hasattr(self.request.user, 'county') and self.request.user.county:
            queryset = queryset.filter(counties__contains=[self.request.user.county])
        
        return queryset
    
    def perform_create(self, serializer):
        alert = serializer.save(created_by=self.request.user)
        # Send alert to users
        AlertService.send_alert(alert)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active alerts"""
        now = timezone.now()
        alerts = Alert.objects.filter(
            status='active',
            start_time__lte=now,
            end_time__gte=now
        )
        
        # Filter by user's county
        if hasattr(request.user, 'county') and request.user.county:
            alerts = alerts.filter(counties__contains=[request.user.county])
        
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        notes = request.data.get('notes', '')
        
        acknowledgment, created = AlertAcknowledgment.objects.get_or_create(
            alert=alert,
            user=request.user,
            defaults={'notes': notes}
        )
        
        if created:
            # Update acknowledgment count
            alert.acknowledgment_count += 1
            alert.save(update_fields=['acknowledgment_count'])
        
        return Response({
            'message': 'Alert acknowledged',
            'already_acknowledged': not created
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsHQAnalyst])
    def cancel(self, request, pk=None):
        """Cancel an alert"""
        alert = self.get_object()
        alert.status = 'cancelled'
        alert.save(update_fields=['status'])
        
        return Response({'message': 'Alert cancelled'})
