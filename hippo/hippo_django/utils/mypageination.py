from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict, namedtuple
class Mypagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 30  # 最大限制





    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code',200),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
