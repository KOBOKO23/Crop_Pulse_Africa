"""
URL patterns for Weather app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WeatherViewSet, WeatherStationViewSet, WeatherDataViewSet,
    WeatherForecastViewSet, WeatherAdvisoryViewSet
)

router = DefaultRouter()
router.register(r'weather', WeatherViewSet, basename='weather')
router.register(r'stations', WeatherStationViewSet, basename='weather-station')
router.register(r'data', WeatherDataViewSet, basename='weather-data')
router.register(r'forecasts', WeatherForecastViewSet, basename='weather-forecast')
router.register(r'advisories', WeatherAdvisoryViewSet, basename='weather-advisory')

urlpatterns = [
    path('', include(router.urls)),
]
