
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from utils.NewResponse import new_response


class NewModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            print(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200,data=str(e))


    def update(self, request, *args, **kwargs):

        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200,data=str(e))


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200,data=str(e))


    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200,data=str(e))

    # 自定义的
    def details(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200,data=str(e))

    # 定义一个模糊检索的方法
    def _fuzzy_search(self, field_list, search_content ,op='OR'):
        # 从 URL 中取到 query 参数
        q = Q()
        q.connector = op
        for field in field_list:
            q.children.append(Q((f'{field}__icontains', search_content )))
        return q
