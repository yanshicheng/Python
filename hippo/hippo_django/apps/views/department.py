from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.NewResponse import api_response
from utils.NewModelViewSet import NewModelViewSet
# Create your views here.
from utils.DepartmentSerializers import DepartmentSerializer
from utils.DepartmentSerializers import Department_ModelSerializer
from apps import models
from utils.mypageination import Mypagination

class Department(NewModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = Department_ModelSerializer
    def list(self, request):
        try:
            search_content = request.query_params.get('search_content', '')
            if search_content != '':
                queryset = models.Department.objects.all()
                q = self._fuzzy_search(['title', 'count'], search_content)
                queryset = queryset.filter(q)
                paginators = Mypagination()
                page_queryset = paginators.paginate_queryset(queryset, request)
                serializer = Department_ModelSerializer(page_queryset, many=True)
                return paginators.get_paginated_response(serializer.data)
            else:
                queryset = models.Department.objects.all()
                paginators = Mypagination()
                #  2. 调用分页器 分页方法
                page_queryset = paginators.paginate_queryset(queryset, request)
                serializer = Department_ModelSerializer(page_queryset, many=True)
                return paginators.get_paginated_response(serializer.data)
        except Exception as e:
            return api_response(code=10200, data=str(e))