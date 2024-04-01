from rest_framework import serializers
from .models import *


class PowerConfSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=20)
    path = serializers.CharField(max_length=50)
    module_name = serializers.CharField(max_length=20)

    def create(self, validated_data):
        """新建"""
        return PowerConf.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.path = validated_data.get('path', instance.path)
        instance.module_name = validated_data('module_name', instance.module_name)
        instance.save()
        return instance


class RolePowerSerializer(serializers.Serializer):
    role = serializers.IntegerField()
    power = serializers.IntegerField()


class RoleConfSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    power_list = RolePowerSerializer(required=False, source='')

    def create(self, validated_data):
        """创建"""
        return UserInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新"""
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class UserinfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    nickname = serializers.CharField(max_length=20, allow_blank=True)
    title = serializers.CharField(max_length=20, allow_blank=True)
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.CharField(source='user.username', read_only=True, required=False)

    def create(self, validated_data):
        """创建"""
        return UserInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新"""
        instance.name = validated_data.get('name', instance.name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
