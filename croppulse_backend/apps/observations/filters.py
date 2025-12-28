"""
Filters for Observations app
"""
from django_filters import rest_framework as filters
from .models import FarmObservation, CropReport, PestDiseaseReport


class FarmObservationFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = FarmObservation
        fields = ['observation_type', 'status', 'county', 'user']


class PestDiseaseReportFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    severity_min = filters.ChoiceFilter(field_name='severity', lookup_expr='gte', choices=PestDiseaseReport.SEVERITY_LEVELS)
    
    class Meta:
        model = PestDiseaseReport
        fields = ['pest_or_disease', 'severity', 'county', 'is_resolved']
