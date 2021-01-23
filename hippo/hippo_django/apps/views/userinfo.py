from django.contrib import auth
from utils.NewResponse import api_response
from rest_framework.views import APIView
from utils.NewModelViewSet import NewModelViewSet
from ..auth.auth import JwtQueryParamsAuthentication
from ..auth.jwt_auth import create_token, analysis_token
from .. import models
from ..serializers.UserSerializers import UserInfo_ModelSerializer, UserManagement_ModelSerializer
from utils.mypageination import Mypagination
from django.contrib.auth.models import User
class JwtLogin(APIView):
    def get(self):
        pass
    def post(self, request):
        email = request.data.get('email')
        pwd = request.data.get('password')
        user_obj = auth.authenticate(request, email=email, password=pwd)
        if user_obj:
            permission_queryset = user_obj.roles.filter(permissions__isnull=False, permissions__pid__gt=0).values(
                "permissions__id",
                "permissions__title",
                "permissions__slug",
                "permissions__remarks",
                )
            permission_list = []
            # item {'permissions__id': 4, 'permissions__title': '测试权限子', 'permissions__slug': 'test2', 'permissions__remarks': None}
            for item in permission_queryset:
                permission_dic= {
                    'title': item['permissions__title'],
                    'url': item['permissions__slug'],
                    'method': item['permissions__remarks'],
                }
                permission_list.append(permission_dic)
            user_info = {
                'email': user_obj.email,
                'username': user_obj.name,
                'roles': [role.title for role in user_obj.roles.all()]
            }
            print(user_info)
            token = create_token({'permission': permission_list, 'user_info': user_info})
            return api_response(data=token)
                # 获取用户上个页面跳转的 地址 如果没有获取到则设置 默认值
        return api_response(10200, '用户名或密码错误,请重试!')

# 注销函数
class JwtLogout(APIView):
    authentication_classes = [JwtQueryParamsAuthentication, ]
    def post(self, request):
        return api_response(data='ok')

class JwtUserInfo(NewModelViewSet):
    authentication_classes = [JwtQueryParamsAuthentication, ]
    serializer_class = UserInfo_ModelSerializer
    queryset = models.UserInfo.objects.all()
    def list(self, request, *args, **kwargs):
        user_info = analysis_token(request)
        if user_info:
            try:
                queryset = models.UserInfo.objects.filter(email=user_info['user_info']['email'],name=user_info['user_info']['username']).first()
                serializer = self.get_serializer(queryset)
                return api_response(data=serializer.data)
                # return api_response(data={'roles':'admin'})
            except Exception as e:
                return api_response(code=10200,data=str(e))
        else:
            return api_response(data={'xx': 'xxx'})
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return api_response(data=serializer.data)
        except Exception as e:
            return api_response(code=10200,data=str(e))

# 重置密码
class SetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        pwd = request.data.get('password')
        new_pwd = request.data.get('new_password')
        if email and pwd and new_pwd:
            user_obj = auth.authenticate(request, email=email, password=pwd)
            if user_obj:
                user_obj.set_password(new_pwd)
                user_obj.save()
                return api_response(data=f'{user_obj.email} 账户密码修改成功!')
            else:
                return api_response(data='用户或密码错误,请检查重试!')
        else:
            return api_response(data='<email>,<password>,<new_password>为必传参数.')


# 管理员重置密码
class ResetPassword(APIView):
    permission_classes = []
    def post(self, request):
        email = request.data.get('email')
        new_pwd = request.data.get('new_password')
        if email and new_pwd:
            user_obj = models.UserInfo.objects.get(email=email)
            if user_obj:
                user_obj.set_password(new_pwd)
                user_obj.save()
                return api_response(data=f'{user_obj.email} 账户密码修改成功!')
            else:
                return api_response(data='用户或密码错误,请检查重试!')
        else:
            return api_response(data='<email>,<new_password>为必传参数.')





class UserManagement(NewModelViewSet):
    serializer_class = UserManagement_ModelSerializer
    queryset = models.UserInfo.objects.all()
    def list(self, request, *args, **kwargs):
        try:
            search_content = request.query_params.get('search_content', '')
            if search_content != '':
                queryset = models.UserInfo.objects.all()
                q = self._fuzzy_search(['name', 'email'], search_content)
                queryset = queryset.filter(q)
                paginators = Mypagination()
                page_queryset = paginators.paginate_queryset(queryset, request)
                serializer = UserManagement_ModelSerializer(page_queryset, many=True)
                return paginators.get_paginated_response(serializer.data)
            else:
                queryset = models.UserInfo.objects.all()
                paginators = Mypagination()
                #  2. 调用分页器 分页方法
                page_queryset = paginators.paginate_queryset(queryset, request)
                serializer = UserManagement_ModelSerializer(page_queryset, many=True)
                return paginators.get_paginated_response(serializer.data)
        except Exception as e:
            return api_response(code=10200, data=f'{str(e)}')

    def create(self, request, *args, **kwargs):
        try:
            serializer = UserManagement_ModelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = serializer.save()
            user_obj.set_password(serializer.data.get('password'))
            user_obj.save()
            return api_response(data=serializer.data)
        except Exception as e:
            return api_response(code=10200,data=str(e))