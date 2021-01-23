
from utils.NewModelViewSet import NewModelViewSet
from rest_framework.views import APIView
from ..serializers.RoleSerializers import RolesModelSerializer, MenusManagement, PermissionsManagement
from .. import models
from utils.NewResponse import api_response
class RolesManagement(NewModelViewSet):
    serializer_class = RolesModelSerializer
    queryset = models.Roles.objects.all()

class MenusManagements(NewModelViewSet):
    serializer_class = MenusManagement
    queryset = models.Menus.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            pid = request.query_params.get('pid', '')
            print(int(pid), type(int(pid)))
            if pid == '':
                return api_response(code=10200, data='pid 为必传选项')
            elif int(pid) == 0:
                print('进入判断')
                res = []
                queryse = models.Menus.objects.filter(pid=pid).values('id', 'pid', 'title', 'url','roles__title')
                print(queryse)
                for obj in queryse:
                    print(obj)
                    print(obj['id'])
                    children = models.Menus.objects.filter(pid=obj['id']).values(
                        'title',
                        'url',
                        'roles__title')
                    children_dic = []
                    if children:
                        for item in children:
                            print(item)
                            item['roles'] = item['roles__title']

                            children_dic.append(item)
                    obj['hasChildren'] = True
                    obj['children'] = children_dic
                    obj['roles'] = obj['roles__title']
                    res.append(obj)
                return api_response(data=res)
            else:
                queryset = models.Menus.objects.filter(pid=pid)
                if queryset:
                    ser = MenusManagement(queryset, many=True)
                    return api_response(data=ser.data)
                else:
                    return api_response(data='')
        except Exception as e:
            return api_response(code=10200, data=f'{str(e)}')

class PermissionsManagements(NewModelViewSet):
    serializer_class = PermissionsManagement
    queryset = models.Permissions.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            pid = request.query_params.get('pid', '')
            if pid == '':
                return api_response(code=10200, data='pid 为必传选项')
            else:
                queryset = models.Permissions.objects.filter(pid=pid)
                if queryset:
                    ser = PermissionsManagement(queryset, many=True)
                    return api_response(data=ser.data)
                else:
                    return api_response(data=[])

        except Exception as e:
            return api_response(code=10200, data=f'{str(e)}')

class PermissionsAllData(APIView):

    def get(self, request):
        childrens = []
        top_data = list(models.Permissions.objects.filter(pid=0).values("id", "title", ))
        for menu in top_data:
            children = list(
                models.Permissions.objects.filter(pid=menu["id"]).values("id", "title", )
            )
            menu["children"] = children
            childrens.append(menu)
        return api_response(data=childrens)
