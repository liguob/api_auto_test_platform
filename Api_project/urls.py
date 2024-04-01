"""Api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path
from django.views import static
from django.conf import settings

from login.views import *
from django.views.generic import TemplateView
from project_manage.views import *
from project_manage.views_case import *
from project_manage.view_run_api import *
from task_manage.views import *
from project_manage.view_version import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', login_page),
    path('login_auth', login_auth),
    path('logout', logout),
    path('user_detail', user_detail),

    path('index/', TemplateView.as_view(template_name='index.html')),

    path('static_data', static_data),
    path('realtime_data/', realtime_data),

    path('project_edit/', project_edit),
    path('project_list/', project_list),
    path('project_detail', project_detail),
    path('project_delete', project_delete),
    path('project_options', project_options),

    path('version_edit', version_edit),
    path('version_detail', version_detail),
    path('version_list', version_list),
    path('version_delete', version_delete),
    path('version_options', version_options),
    path('version_copy', version_copy),

    path('params_edit', params_edit),
    path('params_list', params_list),
    path('params_detail', params_detail),
    path('params_delete', params_delete),

    path('module_detail', module_detail),
    path('module_options', module_options),
    path('edit_module', edit_module),

    path('env_add/', add_env),
    path('env_delete/', env_delete),
    path('env_list/', env_list),

    path('api_edit', api_edit),
    path('api_delete', api_delete),
    path('api_list', api_list),
    path('api_detail', api_detail),

    path('public_notice_list/', public_notice_list),
    path('public_notice_add/', public_notice_add),
    path('public_notice_delete/', public_notice_delete),

    path('base_user', base_user),

    path('menu_power/', menu_power),
    path('power_list/', power_list),

    path('testcase_list', testcase_list),
    path('remove_case/', remove_case),
    path('add_case/', add_case),
    path('change_case_status', change_case_status),
    path('save_case', save_case),
    path('case_detail/', case_detail),
    path('run_api/', run_api),
    path('run_apis/', run_apis),
    path('add_case_api/', add_case_api),
    path('copy_case_api', copy_case_api),
    path('del_case_api', del_case_api),
    path('add_case_conf/', add_case_conf),
    path('del_case_conf/', del_case_conf),
    path('upload_binary_file/', upload_binary_file),
    path('upload_form_data_file/', upload_form_data_file),
    path('save_form_data/', save_form_data),
    path('remove_binary_file/', remove_binary_file),
    path('project_option', project_option),
    path('get_func', get_func),
    path('get_exec', get_exec),
    path('delete_depend_case', delete_depend_case),
    path('add_depend_case', add_depend_case),
    path('case_depend', case_depend),

    path('save_task', save_task),
    path('task_delete', task_delete),
    path('get_jenkins_time', get_jenkins_time),
    path('task_list', task_list),
    path('task_detail', task_detail),
    path('run_task', run_task),
    path('report_task', report_task),
    path('report_testcase', report_testcase),
    path('report_detail', report_detail),
    path('report_testcase_static', report_testcase_static),

    path('debug_report', debug_report),
    path('debug_report_detail', debug_report_detail),
    path('clear_report', clear_report),

    path('get_jsonpath', get_jsonpath),
    path('update_mock', update_mock),
    path('update_exec', update_exec),
]

if not settings.DEBUG:
    urlpatterns.append(
        re_path(r'^static/(?P<path>.*)', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'))
