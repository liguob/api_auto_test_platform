import json
import os.path
import shutil
import threading

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse

from common.common_fun import CJsonEncode
from .models import *
from .views_case import version_file_path


def version_edit(request):
    """新增编辑项目版本"""
    data = json.loads(request.body.decode('utf-8'))
    if 'id' in data:
        ProjectVersionManage.objects.filter(id=int(data['id'])).update(**data)
        version_id = data['id']
    else:
        version_id = ProjectVersionManage.objects.create(**data).id
    res = {'id': version_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def version_detail(request):
    """获取单个版本详情"""
    version_id = int(request.GET.get('id'))
    version_data = list(ProjectVersionManage.objects.filter(id=version_id).values())[0]
    project_data = list(ProjectManage.objects.filter(project_id=version_data['project_id']).values())[0]
    res = {'version_data': version_data, 'project_data': project_data, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def copy_version_data(old_version_id, new_version_id):
    """处理复制版本数据"""
    old_case = TestCase.objects.filter(version__id=old_version_id)
    new_version = ProjectVersionManage.objects.get(id=new_version_id)
    # 复制用例
    for case in old_case:
        old_case_id = case.id
        case.pk = None
        case.version = new_version
        case.copy_from_case_id = old_case_id  # 保存复制来源的用例id
        case.save()
        # 复制接口
        old_case_apis = CaseApi.objects.filter(case_id=old_case_id)
        for api in old_case_apis:
            old_tree_id = api.tree_id
            api.pk = None
            api.version = new_version
            api.case = case
            api.save()
            # 复制配置
            old_confs = ApiConf.objects.filter(api_id=old_tree_id)
            for conf in old_confs:
                conf.pk = None
                conf.api = api
                conf.version = new_version
                conf.save()
            # 复制文件
            old_file_path = version_file_path([old_version_id, old_case_id, old_tree_id])
            if os.path.exists(old_file_path):
                for root, dirs, files in os.walk(old_file_path):
                    if files:
                        new_file_path = version_file_path([case.version_id, case.id, api.tree_id])
                        shutil.copytree(old_file_path, new_file_path)
                        break
    # 复制前置用例
    depend_ship = TestCaseDepends.objects.filter(version_id=old_version_id)
    for i in depend_ship:
        i.id = None
        i.version = new_version
        i.case_id = TestCase.objects.get(Q(copy_from_case_id=i.case_id) & Q(version_id=new_version_id)).id  # 更新id
        i.depend_case_id = TestCase.objects.get(Q(copy_from_case_id=i.depend_case_id) & Q(version_id=new_version_id)).id
        i.save()
    # 复制版本参数
    version_params = VersionParamsManage.objects.filter(Q(version__id=old_version_id) & Q(is_share=True))
    for param in version_params:
        param.pk = None
        param.version = new_version
        param.save()


def version_copy(request):
    """复制版本"""
    copy_data = json.loads(request.body.decode('utf-8'))
    # 复制用例信息
    old_version_id = copy_data['id']
    del copy_data['id']
    version = ProjectVersionManage.objects.create(**copy_data)
    task = threading.Thread(target=copy_version_data, args=(old_version_id, version.id))
    task.start()
    res = {'id': version.id, 'message': '复制任务已执行，请稍后查看数据', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def version_list(request):
    """获取版本列表详情"""
    filter_dict = {'is_delete': False, 'project__is_delete': False}
    version_name = request.GET.get('version_name')
    if version_name:
        filter_dict['version_name__contains'] = version_name
    page = Paginator(list(ProjectVersionManage.objects.filter(**filter_dict).values()),
                     per_page=int(request.GET.get('PageSize')))
    data = page.page(int(request.GET.get('Page'))).object_list
    for i in range(len(data)):
        data[i]['project_name'] = ProjectManage.objects.get(project_id=data[i]['project_id']).project_name
    res = {'data': page.page(int(request.GET.get('Page'))).object_list, 'count': page.count, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def version_delete(request):
    """删除版本"""
    version_id = int(request.GET.get('id'))
    version = ProjectVersionManage.objects.get(id=version_id)
    version.is_delete = True
    version.save()
    res = {'id': version_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def version_options(request):
    """项目项目的版本信息"""
    project_id = int(request.GET.get('project_id'))
    data = list(ProjectVersionManage.objects.filter(project_id=project_id).values('id', 'version_name'))
    res = {'data': data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def params_edit(request):
    """版本参数新增修改"""
    data = json.loads(request.body.decode('utf-8'))
    if 'id' in data:
        param_id = data['id']
        del data['id']
        VersionParamsManage.objects.filter(id=param_id).update(**data)
    else:
        params = VersionParamsManage.objects.create(**data)
        param_id = params.id
    res = {'id': param_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def params_list(request):
    """版本参数列表"""
    query_dict = {}
    version_id = request.GET.get('version_id')
    project_id = request.GET.get('project_id')
    param_name = request.GET.get('key')
    host = request.GET.get('host')
    if version_id:
        query_dict['version_id'] = int(version_id)
    if project_id:
        query_dict['project_id'] = int(project_id)
    if param_name:
        query_dict['key__contains'] = param_name
    if host:
        query_dict['run_env__contains'] = host
    page = Paginator(list(VersionParamsManage.objects.filter(**query_dict).order_by('-is_share').values()),
                     per_page=int(request.GET.get('PageSize')))
    data = page.page(int(request.GET.get('Page'))).object_list
    for i in range(len(data)):
        bind_case_id = data[i]['bind_case_id']
        data[i]['case_name'] = TestCase.objects.get(id=bind_case_id).name if bind_case_id else ''
    res = {'data': data, 'count': page.count, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def params_detail(request):
    """单个参数详情"""
    data = list(VersionParamsManage.objects.filter(id=int(request.GET.get('id'))).values())[0]
    res = {'data': data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def params_delete(request):
    """删除参数"""
    param_id = int(request.GET.get('id'))
    VersionParamsManage.objects.filter(id=param_id).delete()
    res = {'id': param_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
