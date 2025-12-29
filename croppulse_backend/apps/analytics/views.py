"""
Views for Analytics app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import AnalyticsService
from core.permissions import CanAccessAnalytics


class AnalyticsViewSet(viewsets.GenericViewSet):
    """Analytics and dashboard endpoints"""
    
    permission_classes = [IsAuthenticated, CanAccessAnalytics]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get comprehensive dashboard data"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 30))
        
        data = AnalyticsService.get_comprehensive_dashboard(county, days)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get user statistics"""
        county = request.query_params.get('county')
        data = AnalyticsService.get_user_statistics(county)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def weather(self, request):
        """Get weather statistics"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 30))
        data = AnalyticsService.get_weather_statistics(county, days)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def observations(self, request):
        """Get observation statistics"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 30))
        data = AnalyticsService.get_observation_statistics(county, days)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def pest_disease(self, request):
        """Get pest/disease statistics"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 30))
        data = AnalyticsService.get_pest_disease_statistics(county, days)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get alert statistics"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 30))
        data = AnalyticsService.get_alert_statistics(county, days)
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def community(self, request):
        """Get community statistics"""
        days = int(request.query_params.get('days', 30))
        data = AnalyticsService.get_community_statistics(days)
        return Response(data)
