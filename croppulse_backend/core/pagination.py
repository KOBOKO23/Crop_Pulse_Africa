"""
Custom pagination classes for CropPulse Africa API
"""
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination with 20 items per page"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size', self.page_size),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination for large datasets with 50 items per page"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size', self.page_size),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class SmallResultsSetPagination(PageNumberPagination):
    """Pagination for small datasets with 10 items per page"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size', self.page_size),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class TimelineCursorPagination(CursorPagination):
    """
    Cursor-based pagination for timeline/feed views
    Ordered by created_at descending (newest first)
    """
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'


class NotificationPagination(PageNumberPagination):
    """Pagination specifically for notifications"""
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('unread_count', self.get_unread_count()),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_unread_count(self):
        """Override in view to provide unread count"""
        return getattr(self, 'unread_count', 0)
