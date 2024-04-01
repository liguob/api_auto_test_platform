import json
import os
import shutil

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse

from common.common_fun import CJsonEncode
from common.random_data import timestamp
from .models import *
from django.forms.models import model_to_dict


def version_file_path(path: list):
    """根据path层级返回路径"""
    return os.path.abspath(os.path.join('tmp/', *[str(i) for i in path]))


def testcase_list(request):
    """获取项目的用例"""
    res = []
    query_fields = dict()
    status = str(request.GET.get('status'))
    if status.isdigit():
        query_fields['is_active'] = True if int(status) == 1 else False
    if request.GET.get('case_type'):
        query_fields['case_type'] = int(request.GET.get('case_type'))
    if request.GET.get('user'):
        query_fields['user'] = int(request.GET.get('user'))
    if request.GET.get('caseName'):
        query_fields['name__contains'] = request.GET.get('caseName')
    if request.GET.get('version_id'):
        query_fields['version_id'] = int(request.GET.get('version_id'))
    if request.GET.get('moduleId'):
        module_path = ProjectModuleManage.objects.get(id=int(request.GET.get('moduleId'))).module_path
        module_id = [i['id'] for i in
                     list(ProjectModuleManage.objects.filter(module_path__startswith=module_path).values(*['id']))]
        query_fields['module__id__in'] = module_id
    if request.GET.get('project_id'):
        query_fields['project_id'] = int(request.GET.get('project_id'))
    data = Paginator(TestCase.objects.filter(**query_fields), request.GET.get('PageSize'))
    c_page = data.page(int(request.GET.get('Page')))
    for i in c_page:
        res.append({'name': i.name, 'user': i.user.first_name, 'des': i.des, 'id': i.id,
                    'module': i.module.module_name if i.module else '',
                    'priority': i.priority if i.priority else '',
                    'is_active': i.is_active
                    })
    res = {"data": res, "total": data.count}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def change_case_status(request):
    """启用/禁用用例"""
    case = TestCase.objects.get(id=int(request.GET.get('id')))
    case.is_active = False if case.is_active else True
    case.save()
    res = {'id': case.id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def add_case(request):
    """新增用例或复制用例"""
    user_id = request.user.id
    data = json.loads(request.body)
    data['user'] = User.objects.get(id=user_id)
    case = TestCase.objects.create(**data)
    res = {'id': case.id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def remove_case(request):
    """删除用例"""
    case_id = int(request.GET.get('id'))
    user_id = request.user.id
    case = TestCase.objects.get(id=case_id)
    if case.user_id == user_id or User.objects.get(id=user_id).is_superuser:
        depend_case = TestCase.objects.filter(depend_id=case_id)
        if depend_case:
            res = {'message': '该用例属于其他用例的前置步骤，请先删除前置关系', 'type': 'error'}
        else:
            file_path = version_file_path([case.version_id, case.id])
            case.delete()
            res = {'message': '成功', 'type': 'success'}
            # 删除文件
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
    else:
        res = {'message': '操作失败：你不是用例责任人', 'type': 'error'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def case_detail(request):
    """获取用例数据"""
    case_id = request.GET.get('case_id')
    case_data = list(TestCase.objects.filter(id=case_id).values())[0]
    case_data['dek'] = eval(case_data['dek'])
    apis = list(CaseApi.objects.filter(case_id=case_id).values())
    for i in range(len(apis)):
        apis[i]['params'] = eval(apis[i]['params'])
        apis[i]['headers'] = eval(apis[i]['headers'])
        apis[i]['payload_fd'] = eval(apis[i]['payload_fd'])
        apis[i]['payload_xwfu'] = eval(apis[i]['payload_xwfu'])
        confs = list(ApiConf.objects.filter(api_id=apis[i]['tree_id']).values())
        apis[i]['children'] = confs
    case_data['api_data'] = apis
    del case_data['depend_id']
    res = {"caseData": case_data, "message": "成功", "type": "success"}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def case_depend(request):
    """获取用例的前置用例数据"""
    case_id = int(request.GET.get('case_id'))
    depend_cases = TestCaseDepends.objects.filter(case_id=case_id)
    res = {'data': [], 'message': '成功'}
    for case in depend_cases:
        depend_case = TestCase.objects.get(id=case.depend_case_id)
        res['data'].append(
            {'id': case.id, 'user': depend_case.user.first_name, 'name': depend_case.name,
             'case_id': case.depend_case_id,
             'module': depend_case.module.module_name or '', 'des': depend_case.des})
    # depend_id = TestCase.objects.get(id=case_id).depend_id
    # if depend_id:
    #     depend_case = TestCase.objects.get(id=depend_id)
    #     depend_data = {'id': depend_case.id,
    #                    'user': depend_case.user.first_name,
    #                    'name': depend_case.name,
    #                    'module': depend_case.module.module_name if depend_case.module else '',
    #                    'des': depend_case.des
    #                    }
    #     res['data'].append(depend_data)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def delete_depend_case(request):
    """删除用例的前置用例"""
    ID = int(request.GET.get('id'))
    case = TestCaseDepends.objects.get(id=ID)
    case.delete()
    res = {'id': ID, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def add_depend_case(request):
    """新增用例的前置用例"""
    case_id = int(request.GET.get('id'))
    depend_id = int(request.GET.get('depend_id'))
    plan_run_case = [case_id]  # 添加后计划运行的父结点用例
    parent_case_ids = [case_id]  # 初始父结点列表
    while parent_case_ids:
        parent_case_ids = [i['case_id'] for i in
                           list(TestCaseDepends.objects.filter(depend_case_id__in=parent_case_ids).values('case_id'))]
        plan_run_case.extend(parent_case_ids)
    # 判断子结点用例是否在父结点用例中造成循环
    child_case_ids = [depend_id]  # 初始子节点列表
    while child_case_ids:
        for i in child_case_ids:
            if i in plan_run_case:
                circle_name = TestCase.objects.get(id=i).name
                res = {'message': f'添加该前置用例会导致用例：{circle_name}出现无限循环，请重新确认', 'type': 'error'}
                return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode),
                                    content_type='application/json')
        child_case_ids = [j['depend_case_id'] for j in
                          list(TestCaseDepends.objects.filter(case_id__in=child_case_ids).values('depend_case_id'))]
    # 没有导致循环则新增前置
    data = {'case_id': case_id, 'depend_case_id': depend_id, 'version_id': TestCase.objects.get(id=case_id).version_id}
    depend_data = TestCaseDepends.objects.create(**data)
    res = {'id': depend_data.id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def add_case_api(request):
    """测试用例新增接口"""
    case_info = json.loads(request.body.decode('utf-8'))
    CaseApi.objects.filter()
    case_info['priority'] = CaseApi.objects.filter(case_id=case_info['case_id']).count()  # 设置优先级
    case_api = CaseApi.objects.create(**case_info)
    case_api.version = case_api.case.version
    case_api.save()
    api_data = model_to_dict(case_api)
    api_data['params'] = eval(api_data['params'])
    api_data['headers'] = eval(api_data['headers'])
    api_data['payload_fd'] = eval(api_data['payload_fd'])
    api_data['payload_xwfu'] = eval(api_data['payload_xwfu'])
    res = {"data": {**api_data, 'children': []}, "message": "成功", "type": "success"}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def copy_case_api(request):
    """复制接口"""
    copy_id = int(request.GET.get('id'))
    api = CaseApi.objects.get(tree_id=copy_id)
    api.pk = None
    api.priority = CaseApi.objects.filter(case=api.case).count()
    # 置空binary文件
    api.payload_binary_original_name = ''
    api.payload_binary_name = ''
    fd = eval(api.payload_fd)
    for i in range(len(fd)):
        # 如果是文件则置空
        if fd[i]['isFile']:
            fd[i]['isFile'] = False
            fd[i]['value'] = fd[i]['file_name'] = ''
    api.payload_fd = str(fd)
    api.save()
    api_data = model_to_dict(api)
    api_data['params'] = eval(api_data['params'])
    api_data['headers'] = eval(api_data['headers'])
    api_data['payload_fd'] = eval(api_data['payload_fd'])
    api_data['payload_xwfu'] = eval(api_data['payload_xwfu'])
    res = {"data": {**api_data, 'children': []}, "message": "成功", "type": "success"}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def del_case_api(request):
    """删除用例接口"""
    case_id = request.GET.get('case_id')
    tree_id = request.GET.get('tree_id')
    api = CaseApi.objects.get(Q(case_id=case_id) & Q(tree_id=tree_id))
    res = {"api_id": api.tree_id, "message": "成功", "type": "success"}
    file_path = version_file_path([api.version_id, api.case_id, api.tree_id])
    api.delete()
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def add_case_conf(request):
    """测试用例接口新增配置"""
    conf = ApiConf.objects.create(**json.loads(request.body.decode('utf-8')))
    conf.version = conf.api.case.version
    conf.save()
    res = {'data': model_to_dict(conf), 'message': "成功", "type": "success"}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def del_case_conf(request):
    """测试用例接口删除配置"""
    conf_id = request.GET.get('conf_id')
    conf = ApiConf.objects.get(conf_id=int(conf_id))
    conf.delete()
    res = {'conf_id': conf_id, 'message': "成功", "type": "success"}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def save_case(request):
    """保存测试用例"""
    case_info = json.loads(request.body.decode('utf-8'))
    case_data = case_info['data']
    # 保存api接口
    case_id = int(request.GET.get('case_id'))
    if 'api_data' in case_data:
        api_data = case_data.pop('api_data')
        if not case_data['priority']:  # 前端传值为空字符串
            case_data['priority'] = None
        TestCase.objects.filter(id=case_id).update(**case_data)
        for i in range(len(api_data)):
            confs = api_data[i].pop('children')
            api_data[i]['priority'] = i
            CaseApi.objects.filter(tree_id=api_data[i]['tree_id']).update(**api_data[i])
            # 保存配置
            for j in range(len(confs)):
                confs[j]['priority'] = j
                ApiConf.objects.filter(conf_id=confs[j]['conf_id']).update(**confs[j])
    else:
        TestCase.objects.filter(id=case_id).update(**case_data)
    return case_detail(request)


def save_form_data(request):
    tree_id = request.GET['tree_id']
    action = request.GET['action']
    row = int(request.GET['row'])
    form_data = json.loads(request.body.decode('utf-8'))
    # 先保存
    api = CaseApi.objects.get(tree_id=tree_id)
    api.payload_fd = str(form_data)
    api.save()
    if action == 'upload':
        # 上传文件
        api.payload_fd = str(form_data)
    elif action == 'removeFile':
        # 删除行的文件
        payload_fd = eval(api.payload_fd)
        file_path = version_file_path([api.version_id, api.case_id, api.tree_id, payload_fd[row]['file_name']])
        if os.path.exists(file_path):
            os.remove(file_path)
        payload_fd[row]['isFile'] = False
        payload_fd[row]['value'] = payload_fd[row]['file_name'] = ''
        api.payload_fd = str(payload_fd)
    else:
        # 删除行
        payload_fd = eval(api.payload_fd)
        tmp = payload_fd.pop(row)
        file_path = version_file_path([api.version_id, api.case_id, api.tree_id, tmp['file_name']])
        if os.path.exists(file_path):
            os.remove(file_path)
        api.payload_fd = str(payload_fd)
    api.save()
    res = {'api_id': tree_id, 'form_data': eval(api.payload_fd), 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def upload_form_data_file(request):
    """上传form-data文件"""
    case_id = request.GET['case_id']
    api_id = request.GET['tree_id']
    origin_file = request.FILES.get('file')
    case = TestCase.objects.get(id=int(case_id))
    file_name = f'{timestamp()}-{origin_file}'
    file_path = version_file_path([case.version_id, case.id, api_id])
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 上传到服务器
    with open(os.path.join(file_path, file_name), 'wb+') as f:
        for i in origin_file.chunks():
            f.write(i)
    res = {
        'value': str(origin_file), 'file_name': file_name, 'isFile': True,
        'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def upload_binary_file(request):
    case_id = request.GET['case_id']
    tree_id = request.GET['tree_id']
    case = TestCase.objects.get(id=int(case_id))
    origin_file = request.FILES.get('file')
    file_name = f'{timestamp()}-{origin_file}'
    file_path = version_file_path([case.version_id, case.id, tree_id])
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    new_file_path = os.path.join(file_path, file_name)
    with open(new_file_path, 'wb+') as f:
        for i in origin_file.chunks():
            f.write(i)
    fields = {'payload_binary_name': file_name,
              'payload_binary_original_name': str(origin_file)}
    CaseApi.objects.filter(Q(case_id=case_id) & Q(tree_id=tree_id)).update(**fields)
    res = {**fields, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def remove_binary_file(request):
    case_id = request.GET['case_id']
    tree_id = request.GET['tree_id']
    api = CaseApi.objects.get(Q(case_id=case_id) & Q(tree_id=tree_id))
    file_path = version_file_path([api.version_id, api.case_id, api.tree_id, api.payload_binary_name])
    if os.path.exists(file_path):
        os.remove(file_path)
    api.payload_binary_name = api.payload_binary_original_name = ''
    api.save()
    res = {'api_id': api.tree_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
