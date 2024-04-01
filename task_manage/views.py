import json
import threading
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from project_manage.models import *
from project_manage.view_run_api import GenerateReport
from task_manage.models import *
from common.common_fun import CJsonEncode
import datetime
from python_jenkins_monitor.python_jenkins_monitor import get_next_time
from jsonpath import JSONPath


# Create your views here.

def project_option(request):
    # 获取项目选项
    data = list(ProjectManage.objects.filter(is_delete=False).values(*['project_id', 'project_name']))
    res = {'data': data, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def task_list(request):
    # 查询任务列表
    query_dict = {}
    project_id = request.GET.get('project_id')
    version_id = request.GET.get('version_id')
    name = request.GET.get('name')
    if name:
        query_dict['name__contains'] = name
    if project_id:
        query_dict['project_id'] = project_id
    if version_id:
        query_dict['version_id'] = version_id
    page = Paginator(list(TaskManage.objects.filter(**query_dict).values()), per_page=int(request.GET.get('PageSize')))
    data = page.page(int(request.GET.get('Page'))).object_list
    for i in range(len(data)):
        if not data[i]['task_status']:
            data[i]['next_time'] = '无'
        data[i]['project_name'] = ProjectManage.objects.get(project_id=data[i]['project_id']).project_name
    res = {'data': data, 'count': page.count, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def task_detail(request):
    # 查询单个任务详情
    task_id = int(request.GET.get('task_id'))
    data = list(TaskManage.objects.filter(id=task_id).values())[0]
    res = {'data': data, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def cal_jenkins_plan(jenkins_plan: str):
    """返回计算jenkins日常表下一次计划时间"""
    res = None
    if len(jenkins_plan.strip().split(' ')) == 5:
        next_time = get_next_time(jenkins_plan)
        res = datetime.datetime.fromtimestamp(next_time) if next_time else next_time
    return res


def save_task(request):
    # 新增或保存任务
    task_data = json.loads(request.body.decode('utf-8'))
    task_id = task_data.get('id', None)
    if 'jenkins_plan' in task_data:
        next_time = cal_jenkins_plan(task_data['jenkins_plan'])
        if not next_time:
            res = {'message': '日程表格式错误，请重新确认', 'type': 'error'}
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
        task_data['next_time'] = next_time
    if task_id:
        TaskManage.objects.filter(id=task_id).update(**task_data)
        if task_data['task_status']:
            task = TaskManage.objects.get(id=task_id)
            task.next_time = cal_jenkins_plan(task.jenkins_plan)
            task.save()
    else:
        task = TaskManage.objects.create(**task_data)
        task_id = task.id
    res = {'id': task_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def task_delete(request):
    """删除任务"""
    task_id = int(request.GET.get('id'))
    TaskManage.objects.filter(id=task_id).delete()
    res = {'id': task_id, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def run_task(request):
    """接口运行任务"""
    task_id = request.GET.get('id')
    task = threading.Thread(target=do_task, name=task_id, args=(task_id, 'human'))
    task.start()
    res = {'id': task_id, 'message': '任务开始执行，可查看报告', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def report_task(request):
    """接口返回对应task的报告列表"""
    query_dict = {}
    task_id = request.GET.get('task_id')
    host = request.GET.get('host')
    task_name = request.GET.get('task_name')
    project_id = request.GET.get('project_id')
    version_id = request.GET.get('version_id')
    if task_name:
        query_dict['task__name__contains'] = task_name
    if task_id:
        query_dict['task_id'] = int(task_id)
    if host:
        query_dict['host__contains'] = host
    if project_id:
        query_dict['project_id'] = project_id
    if version_id:
        query_dict['version_id'] = version_id
    all_report = Paginator(list(ReportTask.objects.filter(**query_dict).values()),
                           per_page=int(request.GET.get('PageSize')))
    page_task = all_report.page(int(request.GET.get('Page'))).object_list
    res = {'data': page_task, 'count': all_report.count, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def do_task(task_id: int, who: str = 'robot'):
    """实际运行任务"""
    task = TaskManage.objects.get(id=task_id)
    task.status = '运行'
    task.save()
    testcases = []
    task_data = {'task': task,
                 'project': task.project,
                 'version': task.version,
                 'web_type': task.web_type,
                 'host': task.host,
                 'who': who}
    reportTask = ReportTask.objects.create(**task_data)
    run_env = task.web_type + '://' + task.host  # 运行环境
    if who == 'robot':
        task.next_time = cal_jenkins_plan(task.jenkins_plan)
    if task.is_run_before:
        # 前置用例
        testcases.extend(TestCase.objects.filter(
            Q(case_type=2) & Q(project=task.project) & Q(version=task.version)).order_by('priority'))
        # 清除版本的变量参数
        VersionParamsManage.objects.filter(
            Q(version=task.version) & Q(run_env=run_env)).delete()
    if task.is_run_case:
        testcases.extend(TestCase.objects.filter(
            Q(case_type=1) & Q(project=task.project) & Q(version=task.version)))  # 测试用例
    # 获取版本变量
    v_params = list(
        VersionParamsManage.objects.filter(
            (Q(run_env=run_env) & Q(version=task.version)) | (Q(is_share=True) & Q(version=task.version))).values())
    v_params = {i['key']: i['value'] for i in v_params}
    try:
        # 初始化参数
        report = GenerateReport(web_method=reportTask.web_type, host=reportTask.host, version_params=v_params)
        for case in testcases:
            report.set_testcase(testcase=case)
            report.run_case()
            report.update_report({'report_id': reportTask.id, 'module': case.module, 'user': case.user})
            ReportTestcase.objects.create(**report.reportData)
    finally:
        failed_case_num = ReportTestcase.objects.filter(Q(result=False) & Q(report_id=reportTask.id)).count()
        reportTask.status = '失败' if failed_case_num else '成功'
        reportTask.edit_time = timezone.now()
        reportTask.save()
        task.status = '空闲'
        task.save()


def report_testcase_static(request):
    """获取任务报告的统计信息数据"""
    report_id = int(request.GET.get('report_id'))
    data = ReportTestcase.objects.order_by('user').filter(report_id=report_id). \
        values('user__first_name', 'result').annotate(count_res=Count('result'))
    static = dict()
    for i in data:
        username = i['user__first_name'] if i['user__first_name'] else '无人认领'
        if username in static:
            # 更新为0的值
            static[username][static[username].index(0)] = i['count_res']
        else:
            # 新增没有的数据
            static[username] = [i['count_res'], 0] if i['result'] else [0, i['count_res']]
    # 饼图数据
    case_static = {'case_count': 0, 'pass_percent': '',
                   'static_num': [{'value': 0, 'name': '成功'}, {'value': 0, 'name': '失败'}]}
    # 人员用例柱状图数据
    user_static = {'usernames': [], 'pass_num': [], 'fail_num': []}
    pass_num = fail_num = 0
    for name, nums in static.items():
        user_static['usernames'].append(name)
        user_static['pass_num'].append(nums[0])
        user_static['fail_num'].append(nums[1])
        pass_num += nums[0]
        fail_num += nums[1]
    case_static['case_count'] = pass_num + fail_num
    case_static['static_num'][0]['value'] = pass_num
    case_static['static_num'][1]['value'] = fail_num
    try:
        case_static['pass_percent'] = '{:.2f}%'.format(pass_num / (pass_num + fail_num) * 100)
    except ZeroDivisionError:
        case_static['pass_percent'] = '0%'
    res = {'data': {**case_static, **user_static}, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def report_testcase(request):
    """查看任务用例运行报告列表"""
    query_fields = {'report_id': int(request.GET.get('report_id'))}
    if request.GET.get('user'):
        query_fields['user'] = request.GET.get('user')
    if request.GET.get('caseName'):
        query_fields['case_name__contains'] = request.GET.get('caseName')
    if request.GET.get('caseStatus'):
        query_fields['result'] = True if request.GET.get('caseStatus') == '成功' else False
    fields = ['id', 'user_id', 'report_id', 'module', 'result', 'case_name', 'create_time']
    data = Paginator(list(ReportTestcase.objects.filter(**query_fields).values(*fields)),
                     int(request.GET.get('pagesize')))
    res_data = data.page(int(request.GET.get('page'))).object_list
    for i in range(len(res_data)):
        res_data[i]['username'] = User.objects.get(id=res_data[i]['user_id']).first_name \
            if res_data[i]['user_id'] else ''
        res_data[i]['module'] = ProjectModuleManage.objects.get(id=res_data[i]['module']).module_name \
            if res_data[i]['module'] else ''
    res = {'data': res_data, 'total': data.count, 'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def report_detail(request):
    """查看单个用例报告详情"""
    case_report_id = request.GET.get('id')
    data = ReportTestcase.objects.get(id=case_report_id)
    res = {'id': case_report_id, 'case_name': data.case_name,
           'data': {'data': eval(data.case_data), 'error_info': data.error_info}, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def get_jenkins_time(request):
    """获取日程表下次运行时间"""
    jenkins_plan = request.POST.get('jenkins_plan')
    plan_time = cal_jenkins_plan(jenkins_plan)
    if plan_time:
        res = {'data': plan_time, 'message': '成功'}
    else:
        res = {'data': '', 'message': '警告'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def get_func(request):
    """获取可用的mock变量方法"""
    func = list(MockFun.objects.order_by('type_priority').values())
    data = dict()
    for i in func:
        if i['type_name'] not in data:
            data[i['type_name']] = [{'func_name': i['func_name'], 'func_des': i['func_des']}]
        else:
            data[i['type_name']].append({'func_name': i['func_name'], 'func_des': i['func_des']})
    data = [{'type_name': key, 'data': value} for key, value in data.items()]
    res = {'data': data, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def update_mock(request):
    """更新mock方法"""
    MockFun.objects.all().delete()
    data = [
        {'type_name': '基本变量', 'type_priority': 1, 'func_name': 'pystring()',
         'func_des': '返回指定长度范围内的字母字符串，默认参数：Min=5,Max=5'},
        {'type_name': '基本变量', 'type_priority': 1, 'func_name': 'pyfloat()',
         'func_des': '返回指定位数的浮点数，默认参数：left=2(整数位数),right=2(小数位数),positive=True(正数)'},
        {'type_name': '基本变量', 'type_priority': 1, 'func_name': 'number()',
         'func_des': '返回指定范围的随机整数，默认参数：Min=0,Max=9999'},

        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'date()',
         'func_des': '返回随机日期，默认参数：ftime="%Y-%m-%d"'},
        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'date_time()',
         'func_des': '返回随机时间，默认参数：ftime="%Y-%m-%d %H:%M:%S"'},
        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'calc_datetime()',
         'func_des': '返回根据当前时间计算过去或未来时间，默认参数：ftime="%Y-%m-%d %H:%M:%S", days=0, hours=0, minutes=0, seconds=0'},
        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'month_start_day()',
         'func_des': '返回根据当前月份计算过去或未来月份的开始日期，默认参数：ftime="%Y-%m-%d", months=0, years=0'},
        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'month_end_day()',
         'func_des': '返回根据当前月份计算过去或未来月份的结束日期，默认参数：ftime="%Y-%m-%d", months=0, years=0'},
        {'type_name': '时间变量', 'type_priority': 10, 'func_name': 'timestamp()',
         'func_des': '返回当前时间戳（13位数字）'},

        {'type_name': '个人信息', 'type_priority': 20, 'func_name': 'phone()', 'func_des': '返回随机手机号'},
        {'type_name': '个人信息', 'type_priority': 20, 'func_name': 'email()', 'func_des': '返回随机邮箱'},
        {'type_name': '个人信息', 'type_priority': 20, 'func_name': 'name()',
         'func_des': '返回随机姓名（包含三个字母，避免重名）'},
        {'type_name': '个人信息', 'type_priority': 20, 'func_name': 'idcard()', 'func_des': '返回随机身份证号'},

        {'type_name': '地址信息', 'type_priority': 30, 'func_name': 'address()', 'func_des': '返回随机详细地址'},
        {'type_name': '地址信息', 'type_priority': 30, 'func_name': 'city()', 'func_des': '返回随机城市'},
        {'type_name': '地址信息', 'type_priority': 30, 'func_name': 'province()', 'func_des': '返回随机省份'},
        {'type_name': '地址信息', 'type_priority': 30, 'func_name': 'postcode()', 'func_des': '返回随机邮编'},

        {'type_name': '文本信息', 'type_priority': 30, 'func_name': 'paragraph()',
         'func_des': '返回随机一段文本，默认参数Max=200(文本长度最大值)'},
    ]
    for i in data:
        MockFun.objects.create(**i)
    return HttpResponse({'message': '成功'}, content_type='application/json')


def get_jsonpath(request):
    """"返回jsonpath的匹配结果"""
    data = json.loads(request.body.decode('utf-8'))
    json_data = data['data']
    express = data['express']
    res_data = {'data': '', 'message': '成功'}
    try:
        res = JSONPath(express).parse(json_data)
    except Exception:
        res = 'jsonpath语法错误，请检查'
    res_data['data'] = res
    return HttpResponse(json.dumps(res_data, ensure_ascii=False), content_type='application/json')


def get_exec(request):
    exec_data = list(ExecTip.objects.all().values())
    hash_dict = dict()
    for i in exec_data:
        if i['exec_type'] not in hash_dict:
            hash_dict[i['exec_type']] = [{'label': i['label'], 'exec_value': i['exec_value']}]
        else:
            hash_dict[i['exec_type']].append({'label': i['label'], 'exec_value': i['exec_value']})
    res = {'data': hash_dict, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


def update_exec(request):
    ExecTip.objects.all().delete()
    data = [
        {'label': '设置一个用例数字常量', 'exec_type': 'all', 'exec_value': 'case.set("key", 1)'},
        {'label': '设置一个用例字符串常量', 'exec_type': 'all', 'exec_value': 'case.set("key", "value")'},
        {'label': '设置一个用例的mock函数变量', 'exec_type': 'all', 'exec_value': 'case.set("key", number())'},
        {'label': '设置项目全局变量（仅在基础用例有效）', 'exec_type': 'all',
         'exec_value': 'case.set_project("key", "value")'},

        {'label': '断言响应json对象的message等于成功', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.json["message"]=="成功"')"""},
        {'label': '断言响应json对象的count等于1', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.json["data"]["count"]==1')"""},
        {'label': '断言响应json对象的count不等于0', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.json["data"]["count"]!=0')"""},
        {'label': '断言响应json对象的count大于等于1', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.json["data"]["count"]>=1')"""},
        {'label': '断言响应headers的Connection等于keep-alive', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.headers["Connection"]=="keep-alive"')"""},
        {'label': '断言响应文本包含成功', 'exec_type': 'after',
         'exec_value': """case.do_assert('"成功" in response.text')"""},
        {'label': '断言响应内容长度大于1000', 'exec_type': 'after',
         'exec_value': """case.do_assert('len(response.text) > 1000')"""},
        {'label': '断言响应状态码等于200', 'exec_type': 'after',
         'exec_value': """case.do_assert('response.status == 200')"""},

        {'label': '响应json对象获取authorizationToken', 'exec_type': 'after',
         'exec_value': """case.set('key', response.json["data"]["authorizationToken"])"""},
        {'label': '响应headers获取Connection', 'exec_type': 'after',
         'exec_value': """case.set('key', response.headers['Connection'])"""},
        {'label': '正则表达式提取响应文本获取authorizationToken', 'exec_type': 'after',
         'exec_value': """case.re_find('key', '"authorizationToken":"(.+?)",', response.text)"""},
        {'label': '正则表达式提取响应headers文本获取authorization_token', 'exec_type': 'after',
         'exec_value': """case.re_find('key','authorization_token=(.+?);', response.headersText)"""},
        {'label': 'jsonpath过滤提取响应json中的数据(默认获取列表第一个)', 'exec_type': 'after',
         'exec_value': """case.jsonpath_find('key','$..authorizationToken', response.json)"""},
    ]
    for i in data:
        ExecTip.objects.create(**i)
    return HttpResponse({'message': '成功'}, content_type='application/json')
