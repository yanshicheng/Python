
from .. import models
from rest_framework import serializers

class UserInfo_ModelSerializer(serializers.ModelSerializer):
    department_info = serializers.SerializerMethodField(read_only=True)  # 方法字段
    roles_info = serializers.SerializerMethodField(read_only=True)

    # 方法字段的回调函数
    def get_department_info(self,obj):
        if obj.department.title:
            return obj.department.title
        else:
            return ''
    def get_roles_info(self,obj):
        return [role.title for role in obj.roles.all()]

    class Meta:                 # 元信息
        model = models.UserInfo            # 绑定的表
        fields = ['id', 'email', 'name', 'phone', 'roles',  'roles_info', 'department', 'department_info', 'remarks']
        # 给字段加验证信息
        extra_kwargs = {
            'roles': {'write_only': True},
            'department': {'write_only': True},
        }




class UserManagement_ModelSerializer(serializers.ModelSerializer):
    department_info = serializers.SerializerMethodField(read_only=True)  # 方法字段
    roles_info = serializers.SerializerMethodField(read_only=True)
    # is_active = serializers.BooleanField()
    # 方法字段的回调函数
    def get_department_info(self,obj):
        return obj.department.title
    def get_roles_info(self,obj):
        return [role.title for role in obj.roles.all()]

    class Meta:                 # 元信息
        model = models.UserInfo            # 绑定的表
        fields = ['id', 'email', 'name', 'phone',
                  'is_active','password', 'roles',
                  'roles_info',  'department', 'department_info',
                  'remarks']
        # 给字段加验证信息
        extra_kwargs = {
            'roles': {'write_only': True},
            'department': {'write_only': True},
            'password': {'write_only': True},
        }
