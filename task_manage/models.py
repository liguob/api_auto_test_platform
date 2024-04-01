from project_manage.models import *


# Create your models here.
class TaskManage(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.DO_NOTHING, default=None, null=True)
    name = models.CharField(max_length=100, default='')
    web_type = models.CharField(max_length=10, default='http')
    host = models.CharField(max_length=50, default='')
    is_run_before = models.BooleanField(default=False)  # 是否运行基础用例
    is_run_case = models.BooleanField(default=True)  # 是否运行测试用例
    robot = models.CharField(max_length=2000, default='')
    email = models.CharField(max_length=50, default='')
    next_time = models.DateTimeField(null=True)
    des = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=10, default='空闲')  # 任务执行的状态
    task_status = models.BooleanField(default=True)  # 任务是否可用
    jenkins_plan = models.CharField(max_length=200, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class ReportTask(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(to=TaskManage, on_delete=models.SET(None))
    project = models.ForeignKey(to=ProjectManage, on_delete=models.DO_NOTHING, default=None, null=True)
    version = models.ForeignKey(to=ProjectVersionManage, on_delete=models.DO_NOTHING, default=None, null=True)
    who = models.CharField(default='robot', max_length=20)
    web_type = models.CharField(max_length=10)
    host = models.CharField(max_length=50)
    status = models.CharField(default='运行中', max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return str(self.task.id)


class ReportTestcase(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=200)
    module = models.ForeignKey(to=ProjectModuleManage, on_delete=models.SET(None), default=None, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, default=None)
    report = models.ForeignKey(to=ReportTask, on_delete=models.DO_NOTHING)
    case_data = models.TextField(default='[]')
    result = models.BooleanField(default=True)
    error_info = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.case_name


class MockFun(models.Model):
    """Mock函数"""
    id = models.AutoField(primary_key=True)
    type_priority = models.IntegerField()
    type_name = models.CharField(max_length=20)
    func_name = models.CharField(max_length=50)
    func_des = models.CharField(max_length=200)

    def __str__(self):
        return self.func_name


class ExecTip(models.Model):
    """配置器提示信息"""
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=20)
    exec_type = models.CharField(max_length=20)
    exec_value = models.CharField(max_length=200)

    def __str__(self):
        return self.label
