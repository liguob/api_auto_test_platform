from django.contrib.auth.models import User
from django.db import models
import django.utils.timezone as timezone


# Create your models here.


class ProjectManage(models.Model):
    """项目管理"""
    project_id = models.AutoField(primary_key=True, verbose_name="项目id")
    user = models.ForeignKey(to=User, on_delete=models.SET(''))
    project_name = models.CharField(max_length=50, null=False, verbose_name='项目名称', unique=True)
    description = models.CharField(max_length=100, blank='-', verbose_name='项目描述', default='')
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.project_name


class ProjectVersionManage(models.Model):
    """项目版本管理"""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING)
    version_name = models.CharField(max_length=200)
    version_code = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    des = models.CharField(max_length=200)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.version_name

    class Meta:
        ordering = ['-create_time']


class ProjectModuleManage(models.Model):
    """项目模块管理"""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.CASCADE)
    module_path = models.CharField(max_length=200, default='')
    module_name = models.CharField(max_length=20, default='')
    priority = models.IntegerField(default=None)

    class Meta:
        ordering = ['-module_path']


class EnvManage(models.Model):
    """环境管理"""
    id = models.AutoField(primary_key=True, verbose_name='环境id')
    desc = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=50, default='')
    tag_type = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class ApiManage(models.Model):
    """接口管理"""
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50, default='')
    is_other_port = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    web_method = models.CharField(max_length=20, default='http')
    host = models.CharField(max_length=200, default='')
    path = models.CharField(max_length=200, default='')
    method = models.CharField(max_length=10, default='get')
    activeParams = models.CharField(max_length=20, default='Params')
    params = models.TextField(max_length=4000, default='[]')
    headers = models.TextField(max_length=4000, default='[]')
    payload_method = models.CharField(max_length=10, default='none')
    payload_fd = models.TextField(default='[]')
    payload_xwfu = models.TextField(default='[]')
    raw_method = models.CharField(max_length=20, default='Text')
    raw_data = models.TextField(default='')
    des = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.path


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20, default='')
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.DO_NOTHING, default=None, null=True)
    module = models.ForeignKey(to=ProjectModuleManage, on_delete=models.SET(None), default=None, blank=True, null=True)
    dek = models.CharField(max_length=200, default='[]')  # 默认展开节点
    des = models.CharField(max_length=200, default='')  # 用例描述
    host = models.CharField(max_length=200, default='')
    priority = models.IntegerField(default=None, null=True)
    copy_from_case_id = models.IntegerField(default=None, null=True)  # 复制时来源用例id
    depend_id = models.IntegerField(null=True)  # 依赖用例的id
    case_type = models.IntegerField(default=1)  # 用例的类型，分为常规用例：1, 基础用例：2
    web_method = models.CharField(max_length=10, default='http')
    create_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # 是否激活状态

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class TestCaseDepends(models.Model):
    id = models.AutoField(primary_key=True)
    case = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)  # 用例id
    depend_case_id = models.IntegerField()  # 用例依赖的前置用例
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.CASCADE, null=True)  # 版本


class VersionParamsManage(models.Model):
    """项目版本参数模型"""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.CASCADE)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.CASCADE)
    run_env = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=2000)
    des = models.CharField(max_length=200)
    is_share = models.BooleanField(default=False)
    bind_case = models.ForeignKey(to=TestCase, on_delete=models.SET(None), null=True)


class CaseApi(models.Model):
    tree_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.DO_NOTHING, default=None, null=True)
    case = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)  # 排序优先级
    label = models.CharField(max_length=50, default='http请求')
    web_method = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=20, default='api')
    method = models.CharField(max_length=10, default='get')
    host = models.CharField(max_length=200, default='')
    path = models.CharField(max_length=200, default='')
    disabled = models.BooleanField(default=False)
    is_other_port = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    session_name = models.CharField(max_length=50, default='')
    activeParams = models.CharField(max_length=20, default='Params')
    params = models.TextField(max_length=4000, default='[]')
    headers = models.TextField(max_length=4000, default='[]')
    payload_method = models.CharField(max_length=10, default='none')
    payload_fd = models.TextField(default='[]')
    payload_binary_original_name = models.CharField(max_length=100, default='')
    payload_binary_name = models.CharField(max_length=100, default='')
    payload_xwfu = models.TextField(default='[]')
    raw_method = models.CharField(max_length=20, default='Text')
    raw_data = models.TextField(default='')
    graphQL_q = models.CharField(max_length=4000, default='')
    graphQL_g = models.CharField(max_length=4000, default='')
    status = models.BooleanField(default=True)
    data = models.TextField(default='')

    # children = models.TextField(default='[]')

    # children = '[{"run_time":"before","type":"config","id":"1-1"}]'
    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.label


class ApiConf(models.Model):
    conf_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.DO_NOTHING, default=None, null=True)
    api = models.ForeignKey(to=CaseApi, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, default='config')
    priority = models.IntegerField(default=1)  # 排序优先级
    tree_id = models.CharField(max_length=20)
    label = models.CharField(max_length=20)
    run_time = models.CharField(max_length=20, default='前置处理器')
    disabled = models.BooleanField(default=False)
    do_action = models.CharField(max_length=20000)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.label


class ReportDebugTestcase(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.CASCADE)
    case = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    case_name = models.CharField(max_length=200)
    case_data = models.TextField(default='[]')
    params = models.TextField(default='')
    result = models.BooleanField(default=True)
    error_info = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.case_name
