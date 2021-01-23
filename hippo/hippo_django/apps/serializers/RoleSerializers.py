
from .. import models
from rest_framework import serializers

class RolesModelSerializer(serializers.ModelSerializer):
    class Meta:                 # 元信息
        model = models.Roles            # 绑定的表
        fields = ['id', 'title', 'slug', 'remarks', 'permissions' ]




class PermissionsManagement(serializers.ModelSerializer):
    hasChildren = serializers.SerializerMethodField(read_only=True)
    def get_hasChildren(self,  obj):
        if obj.pid == 0:
            return True
        else:
            return False
    class Meta:                 # 元信息
        model = models.Permissions            # 绑定的表
        fields = ['id', 'title', 'slug', 'remarks', 'pid', 'hasChildren']

class MenusManagement(serializers.ModelSerializer):
    roles_list = serializers.SerializerMethodField(read_only=True)
    hasChildren = serializers.SerializerMethodField(read_only=True)
    def get_hasChildren(self,  obj):
        if obj.pid == 0:
            return True
        else:
            return False
    def get_roles_list(self, obj):
        return [role.id for role in obj.roles.all()]
    class Meta:                 # 元信息
        model = models.Menus            # 绑定的表
        fields = ['id', 'title', 'slug', 'url', 'pid', 'roles_list', 'roles', 'hasChildren']

        extra_kwargs = {
            'roles': {'write_only': True},
        }