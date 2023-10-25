from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        if self.page_size_query_param:
            page_size = min(
                int(request.query_params.get(self.page_size_query_param, self.page_size)),
                self.max_page_size
            )
            if page_size == -1:
                return None
        return page_size

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'limit': self.page_size,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
