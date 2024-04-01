import datetime
import os
import time
import threading

from django.contrib import admin
from multiprocessing import Process

from django.db.models import Q

from .models import *
from django.conf import settings
from task_manage.views import cal_jenkins_plan, do_task

# Register your models here.

admin.site.register(TaskManage)
admin.site.register(ReportTask)
admin.site.register(ReportTestcase)
admin.site.register(MockFun)


def start_xl(name):
    """巡逻进程"""
    print('%s %s 启动' % (name, os.getpid()))
    while True:
        all_task = TaskManage.objects.filter(
            Q(project__is_delete=False) & Q(version__is_delete=False) & Q(task_status=True))
        for task in all_task:
            if task.next_time:
                # 计划运行时间1分钟之内尝试运行任务
                now_time = time.time()
                if 0 <= now_time - time.mktime(task.next_time.timetuple()) <= 60:
                    if task.status == '空闲':
                        s = threading.Thread(target=do_task, name=task.id, args=(task.id,))
                        s.start()
                    else:
                        task.next_time = cal_jenkins_plan(task.jenkins_plan)
                        task.save()
                # 计划运行时间1分钟之外仅刷新下一次时间
                elif now_time - time.mktime(task.next_time.timetuple()) > 60:
                    task.next_time = cal_jenkins_plan(task.jenkins_plan)
                    task.save()
        time.sleep(60)


# xl = threading.Thread(target=start_xl, args=('巡逻线程',))
# xl.start()
