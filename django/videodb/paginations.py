from rest_framework import pagination
from rest_framework.response import Response

class VideoitemsPagination(pagination.PageNumberPagination):
    page_size_query_param = 'perpage'
    max_page_size = 500
    page_query_param = 'page'

    def get_paginated_response(self, data, *args, **kwargs):
      return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })