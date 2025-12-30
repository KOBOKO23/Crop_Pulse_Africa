"""
Custom exceptions for CropPulse Africa application
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class WeatherServiceError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Weather service is temporarily unavailable.'
    default_code = 'weather_service_error'


class SMSServiceError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'SMS service is temporarily unavailable.'
    default_code = 'sms_service_error'


class GeocodingServiceError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Geocoding service is temporarily unavailable.'
    default_code = 'geocoding_service_error'


class InvalidLocationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid location coordinates provided.'
    default_code = 'invalid_location'


class FarmNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Farm not found.'
    default_code = 'farm_not_found'


class ObservationNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Observation not found.'
    default_code = 'observation_not_found'


class AlertNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Alert not found.'
    default_code = 'alert_not_found'


class UnauthorizedActionError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You are not authorized to perform this action.'
    default_code = 'unauthorized_action'


class InsufficientPermissionsError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Insufficient permissions to access this resource.'
    default_code = 'insufficient_permissions'


class InvalidFileTypeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid file type. Please upload a supported file format.'
    default_code = 'invalid_file_type'


class FileSizeLimitExceededError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'File size exceeds the maximum allowed limit.'
    default_code = 'file_size_exceeded'


class DataValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Data validation failed.'
    default_code = 'data_validation_error'


class DuplicateEntryError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A duplicate entry already exists.'
    default_code = 'duplicate_entry'


class RateLimitExceededError(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'
