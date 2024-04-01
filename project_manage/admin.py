from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProjectManage)
admin.site.register(EnvManage)
admin.site.register(TestCase)
admin.site.register(CaseApi)
admin.site.register(ApiConf)
admin.site.register(ReportDebugTestcase)
admin.site.register(ProjectModuleManage)
admin.site.register(ProjectVersionManage)