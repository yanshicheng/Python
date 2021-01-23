from apps.models import Department
from rest_framework import serializers

class DepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)
    count = serializers.IntegerField()


class Department_ModelSerializer(serializers.ModelSerializer):
    class Meta:                 # 元信息
        model = Department            # 绑定的表
        fields = '__all__'      # 所有字段