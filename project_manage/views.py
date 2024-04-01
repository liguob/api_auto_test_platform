import json

from django.core.paginator import Paginator
from django.db.models import Q, Count, F

from common.common_fun import json_http_response, CJsonEncode
from .models import *
from django.http import HttpResponse


# Create your views here.


def project_delete(request):
    """删除项目"""
    project_id = json.loads(request.body)['project_id']
    project = ProjectManage.objects.get(project_id=project_id)
    project.is_delete = True
    project.save()
    res = {'id': project_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def project_edit(request):
    """新增修改项目"""
    req = json.loads(request.body)
    if 'project_id' in req:
        ProjectManage.objects.filter(project_id=req['project_id']).update(**req)
        project_id = req['project_id']
    else:
        project_id = ProjectManage.objects.create(**req).project_id
    res = {'id': project_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def project_options(request):
    """返回项目选项"""
    project_data = list(ProjectManage.objects.filter(is_delete=False).values('project_name', 'project_id'))
    res = {'data': project_data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def project_list(request):
    """查询项目列表"""
    filter_dict = {'is_delete': False}
    if request.GET.get('project_name', None):
        filter_dict['project_name__contains'] = request.GET.get('project_name', None)
    page = Paginator(list(ProjectManage.objects.filter(**filter_dict).values()),
                     per_page=int(request.GET.get('PageSize')))
    res = page.page(int(request.GET.get('Page'))).object_list
    for i in range(len(res)):
        res[i]['create_name'] = User.objects.get(id=res[i]['user_id']).first_name
    res = {'data': res, 'count': page.count, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def project_detail(request):
    """单个项目详情"""
    res = list(ProjectManage.objects.filter(project_id=request.GET['project_id']).values())[0]
    res['project_params'] = eval(res['project_params'])
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def module_detail(request):
    """获取项目的模块详情"""
    project_id = request.GET.get('project_id')
    modules = list(ProjectModuleManage.objects.filter(project_id=project_id).values())
    h = {'': []}
    # 处理子父路径关系，生成结果树el-tree数据
    for i in modules:
        parent_path = i['module_path'].rsplit('/', 1)[0]
        # 存在子节点
        if i['module_path'] in h:
            # 且有兄弟节点
            if parent_path in h:
                h[parent_path].append({**i, 'children': sorted(h[i['module_path']], key=lambda x: x['priority'])})
            else:
                h[parent_path] = [{**i, 'children': sorted(h[i['module_path']], key=lambda x: x['priority'])}]
            del h[i['module_path']]
        # 仅有兄弟节点存在
        elif parent_path in h:
            h[parent_path].append(i)
        else:
            h[parent_path] = [i]
    data = sorted(h[''], key=lambda x: x['priority'])
    res = {'data': data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def module_options(request):
    """获取项目的模块选项信息"""
    project_id = request.GET.get('project_id')
    modules = list(ProjectModuleManage.objects.filter(project_id=int(project_id)).values())[::-1]
    res = {'data': modules, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def edit_module(request):
    """新增，修改或删除模块"""
    data = json.loads(request.body.decode('utf-8'))
    action = request.GET.get('action')
    parent_module = request.GET.get('parent_module')
    data['priority'] = data.get('priority') if data.get('priority') else 0
    if parent_module:
        data['module_path'] = ProjectModuleManage.objects.get(id=int(parent_module)).module_path \
                              + '/' + data['module_name']
    else:
        data['module_path'] = '/' + data['module_name']
    # 删除
    if action == 'del':
        ProjectModuleManage.objects.filter(
            Q(project_id=data['project_id']) & Q(
                module_path__startswith=ProjectModuleManage.objects.get(id=data['id']).module_path)).delete()
        module_id = data['id']
    # 修改
    elif 'id' in data and action == 'edit':
        # 同节点下重名判断
        if ProjectModuleManage.objects.exclude(id=data['id']).filter(module_path=data['module_path']):
            res = {'message': '同级模块不能存在同名模块', 'type': 'error'}
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        c_module = ProjectModuleManage.objects.get(id=data['id'])
        old_module_path = c_module.module_path  # 修改前的path
        c_module.module_name = data['module_name']
        c_module.save()
        modules = ProjectModuleManage.objects.filter(module_path__startswith=old_module_path)
        for i in modules:
            i.module_path = i.module_path.replace(old_module_path, data['module_path'], 1)
            i.save()
        module_id = data['id']
    # 新增
    elif action == 'edit':
        # 同节点下重名判断
        if ProjectModuleManage.objects.filter(module_path=data['module_path']):
            res = {'message': '同级模块不能存在同名模块', 'type': 'error'}
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        module = ProjectModuleManage.objects.create(**data)
        module_id = module.id
    else:
        res = {'message': '参数异常错误', 'type': 'error'}
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
    res = {'id': module_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def env_list(request):
    """获取环境配置"""
    res = list(EnvManage.objects.all().values())
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def env_delete(request):
    """删除环境"""
    env_id = json.loads(request.body.decode('utf-8'))['id']
    EnvManage.objects.filter(id=env_id).delete()
    return env_list(request)


def add_env(request):
    """新增修改环境"""
    req = json.loads(request.body.decode('utf-8'))
    EnvManage.objects.create(**req)
    return env_list(request)


def api_list(request):
    """查询接口"""
    search_key = request.GET.get('search_key')
    if search_key:
        res = list(ApiManage.objects.filter(Q(label__contains=search_key) | Q(path__contains=search_key)).values())
    else:
        res = list(ApiManage.objects.all().values())
    page = Paginator(res, int(request.GET.get('PageSize')))
    page_data = page.page(int(request.GET.get('Page')))
    data = {'data': page_data.object_list, 'count': page.count, 'message': '成功'}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


def api_detail(request):
    """单个接口详情信息"""
    api_id = request.GET.get('id')
    data = list(ApiManage.objects.filter(id=int(api_id)).values())[0]
    data['params'] = eval(data['params'])
    data['headers'] = eval(data['headers'])
    data['payload_fd'] = eval(data['payload_fd'])
    data['payload_xwfu'] = eval(data['payload_xwfu'])
    res = {'data': data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def api_delete(request):
    """删除接口"""
    api_id = request.GET.get('id')
    api = ApiManage.objects.get(id=api_id)
    api.delete()
    res = {'id': api.id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def api_edit(request):
    """新增或编辑接口"""
    req = json.loads(request.body.decode('utf-8'))
    if 'id' in req:
        ApiManage.objects.filter(id=req['id']).update(**req)
        res_id = req['id']
    else:
        res_id = ApiManage.objects.create(**req).id
    res = {'id': res_id, "message": "成功", 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def menu_power(request):
    """判断是否管理员"""
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse(json.dumps({'is_user': True}, ensure_ascii=False), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'is_user': False}, ensure_ascii=False), content_type='application/json')
