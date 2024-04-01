from rest_framework import serializers

from project_manage.models import *


class ProjectManageSerializer(serializers.ModelSerializer):
    create_name = serializers.CharField(source='user.first_name', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = ProjectManage
        exclude = ['edit_time', 'is_delete', 'user']
        read_only_fields = ['case_count', 'api_count']

