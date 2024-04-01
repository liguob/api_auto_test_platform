from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField


# Create your models here.

class PublicNotice(models.Model):
    """公告"""
    notice_id = models.AutoField(primary_key=True)
    content = models.CharField('公告内容', max_length=200, null=False)
    create_date = models.DateField('创建日期', auto_now_add=True)
    expiration_date = models.DateField('失效日期')

    def __str__(self):
        return self.content


class UserInfo(models.Model):
    """用户信息"""
    id = models.AutoField(primary_key=True)
    user = OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, default='', blank=True)
    title = models.CharField(max_length=20, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class PowerConf(models.Model):
    """权限设置表"""
    id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=50, null=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name

# class RoleConf(models.Model):
#     """角色表"""
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     create_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-create_time']
#
#     def __str__(self):
#         return self.name
#
#
# class RolePower(models.Model):
#     """角色权限映射表"""
#     role = models.ForeignKey(to=RoleConf, on_delete=models.CASCADE)
#     power = models.ForeignKey(to=PowerConf, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return
#
#
# class UserRole(models.Model):
#     """用户角色映射表"""
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     role = models.ForeignKey(to=RoleConf, on_delete=models.CASCADE)
