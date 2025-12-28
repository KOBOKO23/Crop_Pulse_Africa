"""
URL patterns for Observations app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmObservationViewSet, CropReportViewSet, PestDiseaseReportViewSet

router = DefaultRouter()
router.register(r'farm-observations', FarmObservationViewSet, basename='farm-observation')
router.register(r'crop-reports', CropReportViewSet, basename='crop-report')
router.register(r'pest-disease-reports', PestDiseaseReportViewSet, basename='pest-disease-report')

urlpatterns = [
    path('', include(router.urls)),
]
