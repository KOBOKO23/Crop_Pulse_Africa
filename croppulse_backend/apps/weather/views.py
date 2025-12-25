"""
Views for Weather app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import WeatherStation, WeatherData, WeatherForecast, WeatherAdvisory
from .serializers import (
    WeatherStationSerializer, WeatherDataSerializer, WeatherDataSimpleSerializer,
    WeatherForecastSerializer, WeatherAdvisorySerializer,
    CurrentWeatherRequestSerializer, ForecastRequestSerializer
)
from .services import WeatherService
from core.permissions import CanAccessAnalytics, IsHQAnalyst
from core.pagination import StandardResultsSetPagination


class WeatherViewSet(viewsets.GenericViewSet):
    """Weather data endpoints"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def current(self, request):
        """Get current weather for coordinates"""
        serializer = CurrentWeatherRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        latitude = float(serializer.validated_data['latitude'])
        longitude = float(serializer.validated_data['longitude'])
        
        try:
            weather_data = WeatherService.fetch_current_weather(latitude, longitude)
            return Response(weather_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'])
    def forecast(self, request):
        """Get weather forecast for coordinates"""
        serializer = ForecastRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        latitude = float(serializer.validated_data['latitude'])
        longitude = float(serializer.validated_data['longitude'])
        days = serializer.validated_data['days']
        
        try:
            forecast_data = WeatherService.fetch_forecast(latitude, longitude, days)
            return Response({'forecasts': forecast_data})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['get'])
    def county_summary(self, request):
        """Get weather summary for a county"""
        county = request.query_params.get('county')
        days = int(request.query_params.get('days', 7))
        
        if not county:
            return Response(
                {'error': 'County parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        summary = WeatherService.get_weather_summary(county, days)
        return Response(summary)


class WeatherStationViewSet(viewsets.ModelViewSet):
    """Weather station management"""
    
    queryset = WeatherStation.objects.all()
    serializer_class = WeatherStationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHQAnalyst()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def recent_data(self, request, pk=None):
        """Get recent weather data from a station"""
        station = self.get_object()
        days = int(request.query_params.get('days', 7))
        
        start_date = timezone.now() - timedelta(days=days)
        
        weather_data = WeatherData.objects.filter(
            station=station,
            recorded_at__gte=start_date
        ).order_by('-recorded_at')
        
        serializer = WeatherDataSimpleSerializer(weather_data, many=True)
        return Response(serializer.data)


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """Historical weather data"""
    
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['county', 'source']
    search_fields = ['county', 'condition']
    ordering_fields = ['recorded_at', 'temperature', 'rainfall']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(recorded_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(recorded_at__lte=end_date)
        
        return queryset


class WeatherForecastViewSet(viewsets.ReadOnlyModelViewSet):
    """Weather forecast data"""
    
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['county', 'forecast_date']
    ordering_fields = ['forecast_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Only show future forecasts by default
        queryset = queryset.filter(forecast_date__gte=timezone.now().date())
        
        return queryset


class WeatherAdvisoryViewSet(viewsets.ModelViewSet):
    """Weather advisory management"""
    
    queryset = WeatherAdvisory.objects.all()
    serializer_class = WeatherAdvisorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['severity', 'is_active']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHQAnalyst()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user's county if provided
        if hasattr(self.request.user, 'county') and self.request.user.county:
            queryset = queryset.filter(counties__contains=[self.request.user.county])
        
        return queryset
    
    def perform_create(self, serializer):
        advisory = serializer.save(created_by=self.request.user)
        # Notifications are sent automatically via service
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active advisories"""
        county = request.query_params.get('county', request.user.county)
        advisories = WeatherService.get_active_advisories(county)
        
        serializer = self.get_serializer(advisories, many=True)
        return Response(serializer.data)
