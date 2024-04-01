import json
import os.path
import re
from jsonpath import JSONPath
from django.forms import model_to_dict
import requests
from string import Template
from urllib.parse import urlencode

from django.http import HttpResponse

from common.common_fun import CJsonEncode
from .models import *
from django.db.models import Q
from random import randint
from project_manage.views_case import save_case, version_file_path
from common.random_data import *


def get_mime(file_name):
    # 多用途互联网邮件扩展类型MIME
    d = {
        'image/png': ['png'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xlsx'],
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['pptx'],
        'application/pdf': ['pdf'],
        'image/jpeg': ['jpg', 'jpeg'],
        'application/zip': ['zip'],
        'text/plain': ['txt'],
        'video/mp4': ['mp4'],
        'application/msword': ['doc', 'dot'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template': ['dotx'],
        'application/vnd.ms-word.document.macroEnabled.12': ['docm'],
        'application/vnd.ms-word.template.macroEnabled.12': ['dotm'],
        'application/vnd.ms-excel': ['xls', 'xlt', 'xla'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.template': ['xltx'],
        'application/vnd.ms-excel.sheet.macroEnabled.12': ['xlsm'],
        'application/vnd.ms-excel.template.macroEnabled.12': ['xltm'],
        'application/vnd.ms-excel.addin.macroEnabled.12': ['xlam'],
        'application/vnd.ms-excel.sheet.binary.macroEnabled.12': ['xlsb'],
        'application/vnd.ms-powerpoint': ['ppt', 'pot', 'pps', 'ppa'],
        'application/vnd.openxmlformats-officedocument.presentationml.slideshow': ['ppsx'],
        'application/vnd.ms-powerpoint.addin.macroEnabled.12': ['ppam'],
        'application/vnd.ms-powerpoint.presentation.macroEnabled.12': ['pptm', 'potm'],
        'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': ['ppsm'],
        'application/x-tar': ['tar'],
    }
    hz = file_name.split('.')[-1]
    for key, value in d.items():
        if hz in value:
            return key
    return 'application/octet-stream'  # 一切未知类型


class Response:

    def __init__(self, response: requests.Response, cookies, headers_text: str):
        try:
            self.json = response.json()
        except:
            self.json = dict()
        self.headers = response.headers
        self.text = response.text
        self.status = response.status_code
        self.cookies = cookies
        self.raw = response.raw
        self.headersText = headers_text


class RunApi:
    v_params_dict = {}

    def __init__(self, testCase: TestCase, api: dict, web_method: str, host: str, tq: dict = None,
                 v_params_dict: dict = None,
                 session_dict: dict = None):
        """初始化接口请求数据"""
        self.testCase = testCase
        self.projectId = testCase.project_id
        self.version_id = testCase.version_id
        self.request_time = 0  # 请求响应时间（毫秒）
        # 判断是否有版本变量传入
        if v_params_dict:
            RunApi.v_params_dict = v_params_dict
        self.tq = tq if tq else RunApi.v_params_dict  # 如果有tq则获取，否则初始化为版本变量
        self.session_dict = session_dict if session_dict else {}
        self.api = api
        self.web_method = web_method if web_method else 'http'
        self.host = host
        self.files = []
        self.method = self.api['method'].upper()
        self.Request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'client': 'pc',
        }
        self.url = ''
        self.path = ''
        self.params = {}
        self.cookies = '[no cookies]'
        self.response = None
        self.Request_body = {}
        self.Response_body = ''
        self.Response_headers = ''
        self.RequestFile_body = ''  # 上传文件时用于显示上传的文件名称，不显示实际的二进制文件内容（太大）
        self.setConfig = []
        self.apiData = {}
        self.result = True

    def do_assert(self, expression: str):
        response = Response(response=self.response, cookies=self.cookies, headers_text=self.Response_headers)
        try:
            res = eval(expression)
            if res is not True:
                # 是否已失败
                if self.setConfig[-1]['result']:
                    self.setConfig[-1]['result'] = self.result = False
                    self.setConfig[-1]['info'] = '失败'
                # 断言失败
                if res is False:
                    tip = f'{expression}: {repr(AssertionError)}'
                # 不是断言语句
                else:
                    tip = f'{expression}: 不是断言语句'
                self.setConfig[-1]['info'] += '\n' + tip
        except Exception as e:
            # 其他异常
            self.set_config_fail(info='断言失败', expression=str(expression), e=e)

    def set(self, key, value):
        # 设置用例的参数
        self.tq.update({key: value})

    def re_find(self, key: str, re_exp: str, all_str: str):
        """正则匹配字符串"""
        res = re.findall(rf'{re_exp}', all_str)[0]
        self.set(key, value=res)

    def jsonpath_find(self, key, expression: str, json_item, is_list=False):
        """使用jsonpath过滤数据"""

        res = JSONPath(expression).parse(json_item)
        if is_list:
            value = res
        else:
            value = res[0] if res else []
        self.tq.update({key: value})

    def set_project(self, key, value, des=''):
        # 设置用例所属的项目参数， 仅在基础用例中使用时有效，否则报错
        if self.testCase.case_type == 2:
            RunApi.v_params_dict.update({key: value})  # 更新版本变量
            self.tq.update({key: value})  # 更新用例变量
            # 更新或创建参数数据
            VersionParamsManage.objects.update_or_create(run_env=self.web_method + '://' + self.host, key=key,
                                                         is_share=False,
                                                         defaults={'value': value, 'bind_case': self.testCase,
                                                                   'des': des,
                                                                   'version': self.testCase.version,
                                                                   'project': self.testCase.project})
        else:
            raise Exception('set_project方法只在基础用例中使用有效')

    def run_config(self, conf_data: dict):
        """前置后置处理器"""
        if not conf_data['disabled']:
            res = {'name': f'{conf_data["run_time"]}-' + conf_data['label'], 'result': True, 'info': '正常\n'}
            self.setConfig.append(res)
            name_space = {**globals(), 'case': self}  # 命名空间
            if conf_data['run_time'] == '后置处理器':
                response = Response(self.response, cookies=self.cookies, headers_text=self.Response_headers)
                name_space['response'] = response  # 后置处理器增加response对象
            for _exec_str in conf_data['do_action'].split('\n'):
                try:
                    do_str = Template(_exec_str).safe_substitute(self.tq)
                    exec(do_str, name_space)
                except Exception as e:
                    self.set_config_fail(info='语句错误', expression=_exec_str, e=e)

    def set_config_fail(self, info: str, expression: str, e: Exception):
        """刷新配置错误信息"""
        if self.setConfig[-1]['result']:
            self.setConfig[-1]['result'] = self.result = False
            self.setConfig[-1]['info'] = '失败\n'
        self.setConfig[-1]['info'] += '\n' + '[%s]\n%s: %s' % (info, expression, repr(e))

    def update_api_data(self):
        """更新运行结果"""
        self.apiData = {
            'name': f'{self.testCase.name}：{self.api["label"]}',
            'status_code': getattr(self.response, 'status_code', '无'),
            'request_time': self.request_time,
            'result': self.result,
            'url': self.url,
            'method': self.method,
            'Response_headers': self.Response_headers,
            'Response_body': self.Response_body,
            'Request_headers': self.Request_headers,
            'Request_body': '%s data:\n\n%s\n\n%s' % (self.method, self.Request_body, self.cookies),
            'setConfig': self.setConfig
        }

    def do_replace(self):
        # path
        self.path = (Template(self.api['path'])).safe_substitute(self.tq)
        # header
        headers = eval(Template(self.api['headers']).safe_substitute(self.tq))
        self.Request_headers.update({i['key']: i['value'] for i in headers if i['key'] and i['value']})
        # params
        params = eval(self.api['params'])
        self.params = {i['key']: Template(i['value']).safe_substitute(self.tq) for i in params if
                       i['key'] or i['value']}
        # none
        if self.api['payload_method'] == 'none':
            self.Request_body = {}
        # form-data
        elif self.api['payload_method'] == 'form-data':
            self.Request_body = {}
            form_data = eval(Template(self.api['payload_fd']).safe_substitute(self.tq))
            for i in form_data:
                self.RequestFile_body += '%s:%s\n' % (i['key'], i['value'])
                if i['isFile']:
                    self.files.append(
                        (i['key'], (i['value'], open(
                            version_file_path([self.version_id, self.testCase.id, self.api['tree_id'], i['file_name']]),
                            'rb'), get_mime(i['value']))))
                else:
                    self.Request_body[i['key']] = i['value']
            self.RequestFile_body = self.RequestFile_body[:-1]  # 删除末尾换行符
        # x-www-form-urlencoded
        elif self.api['payload_method'] == 'x-www-form-urlencoded':
            self.Request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            payload_xwfu = eval(self.api['payload_xwfu'])
            self.Request_body = {i['key']: Template(i['value']).safe_substitute(self.tq) for i in payload_xwfu if
                                 i['key'] or i['value']}
        # raw
        elif self.api['payload_method'] == 'raw':
            headers_dict = {'Text': 'text/plain', 'JavaScript': 'application/javascript', 'JSON': 'application/json',
                            'HTML': 'text/html', 'XML': 'application/xml'}
            self.Request_headers['Content-Type'] = headers_dict[self.api['raw_method']]
            # if self.api['raw_method'] == 'Text':
            #     self.Request_headers['Content-Type'] = 'text/plain'
            # elif self.api['raw_method'] == 'JavaScript':
            #     self.Request_headers['Content-Type'] = 'application/javascript'
            # elif self.api['raw_method'] == 'JSON':
            #     self.Request_headers['Content-Type'] = 'application/json'
            # elif self.api['raw_method'] == 'HTML':
            #     self.Request_headers['Content-Type'] = 'text/html'
            # elif self.api['raw_method'] == 'XML':
            #     self.Request_headers['Content-Type'] = 'application/xml'
            self.Request_body = Template(self.api['raw_data']).safe_substitute(self.tq)
        elif self.api['payload_method'] == 'binary':
            self.Request_headers['Content-Type'] = get_mime(self.api['payload_binary_original_name'])
            try:
                self.Request_body = open(
                    version_file_path(
                        [self.version_id, self.testCase.id, self.api['tree_id'], self.api['payload_binary_name']]),
                    'rb')
            except Exception as e:
                self.Response_body = repr(e)
            self.RequestFile_body += 'src:%s' % self.api['payload_binary_original_name']

    def make_url(self):
        """处理url"""
        if self.api['is_other_port']:
            self.url = self.api['web_method'] + '://' + self.api['host'] + self.api['path']
            self.Request_headers.update({'Host': self.api['host']})
        else:
            self.url = self.web_method + '://' + self.host + self.api['path']
            self.Request_headers.update({'Host': self.host})
        if self.params:
            self.url = self.url + '?' + urlencode(self.params)

    def do_send_api(self):
        # 处理请求数据
        self.do_replace()
        # 处理url
        self.make_url()
        request_data = {'method': self.method,
                        'url': self.url,
                        'headers': self.Request_headers,
                        'data': None,
                        'files': self.files,
                        'timeout': (5, 15)
                        }
        # 请求头
        self.Request_headers = '\n'.join(['%s:%s' % (i, j) for i, j in self.Request_headers.items()])
        try:
            # 请求data
            data = self.Request_body if self.api['raw_method'] != 'JSON' else \
                json.dumps(json.loads(str(self.Request_body)))
            request_data['data'] = data
            if self.api['is_login'] and self.api['session_name']:
                # 创建登录session
                self.session_dict[self.api['session_name']] = requests.session()
                before_send_time = time.time()
                self.response = self.session_dict[self.api['session_name']].request(**request_data)
            elif self.session_dict:
                # 使用session
                if self.api['session_name'] and not self.api['is_login']:
                    self.cookies = 'cookies:\n' + '; '.join(
                        ['%s=%s' % (i, j) for i, j in self.session_dict[self.api['session_name']].cookies.items()])
                    before_send_time = time.time()
                    self.response = self.session_dict[self.api['session_name']].request(**request_data)
                else:
                    before_send_time = time.time()
                    self.response = requests.request(**request_data)
            else:
                # 无session
                before_send_time = time.time()
                self.response = requests.request(**request_data)
            if hasattr(self.response, 'status_code'):
                self.request_time = int((time.time() - before_send_time) * 1000)
            self.Response_body = self.response.content.decode('utf-8', 'ignore')
            self.Response_headers = '\n'.join(['%s:%s' % (i, j) for i, j in self.response.headers.items()])
            if int(self.response.status_code) > 399:
                # 接口状态大于等于400，则判断为失败
                self.result = False
        except Exception as e:
            self.Response_body = repr(e)
            self.Response_headers = '无'
            self.result = False
        finally:
            # 根据请求类型处理请求body
            if self.method == 'get' or self.api['payload_method'] == 'none':
                self.Request_body = '无'
            elif self.api['payload_method'] in ['form-data', 'binary']:
                self.Request_body = self.RequestFile_body
            elif isinstance(self.Request_body, dict):
                self.Request_body = '\n'.join(['%s:%s' % (i, j) for i, j in self.Request_body.items()])

    def run_api(self):
        if not self.api['disabled']:
            for i in self.api['children']:
                if i['run_time'] == '前置处理器':
                    # 执行前置处理器
                    self.run_config(i)
            # 发送请求
            self.do_send_api()
            # 请求成功则执行后置处理器
            if self.response:
                for i in self.api['children']:
                    if i['run_time'] != '前置处理器':
                        self.run_config(i)
            self.update_api_data()


class GenerateReport:
    """生成用例报告类"""

    def __init__(self, version_params: dict, web_method: str, host: str):
        # 用例的变量对象
        self.testcase = None
        self.reportData = {}
        self.session = {}
        self.tq = version_params
        # 项目的变量对象
        self.web_method = web_method
        self.host = host
        self.version_params = version_params

    def set_testcase(self, testcase: TestCase):
        """初始化测试用例数据"""
        self.testcase = testcase
        self.reportData = {'case_name': testcase.name,
                           'case_data': [],
                           'result': True,
                           'error_info': ''}
        self.session = {}
        self.tq = {}

    def update_report(self, data: dict):
        """更新用例报告"""
        self.reportData.update(data)

    def run_api(self, testcase: TestCase, api: CaseApi):
        """运行单个接口,生成报告"""
        # 获取单个接口数据
        api_data = model_to_dict(api)
        api_data['children'] = list(ApiConf.objects.filter(api=api).values())
        # 运行接口
        if self.version_params:
            # 第一次运行时传递项目变量
            api = RunApi(testCase=testcase, api=api_data, web_method=self.web_method, host=self.host, tq=self.tq,
                         v_params_dict=self.version_params,
                         session_dict=self.session)
        else:
            # 不传递项目变量
            api = RunApi(testCase=testcase, api=api_data, web_method=self.web_method, host=self.host, tq=self.tq,
                         session_dict=self.session)
        api.run_api()
        self.tq.update(api.tq)
        self.session.update(api.session_dict)
        self.reportData['case_data'].append(api.apiData)
        # 判断是否失败(单个api结果失败则用例失败或用例没有任何接口请求，用例失败)
        if not api.apiData['result']:
            self.reportData['result'] = False

    def run_case(self):
        """运行单个用例，生成报告"""

        # case_ids = [self.testcase.id]  # 所有需要运行的用例id
        # case_dict = {self.testcase.id: self.testcase}  # 所有需要用例对象字典

        # 递归运行用例
        def run_step_case(case_id):
            step_case_ids = [i['depend_case_id'] for i in
                             TestCaseDepends.objects.filter(case_id=case_id).values('depend_case_id')]
            for j in step_case_ids:
                run_step_case(j)
            apis = CaseApi.objects.filter(Q(case_id=case_id) & Q(disabled=False))
            for api in apis:
                self.run_api(testcase=TestCase.objects.get(id=case_id), api=api)
            # 如果用例没有执行任何请求，则置为失败
            if not self.reportData['case_data']:
                self.reportData['result'] = False

        run_step_case(self.testcase.id)
        # 执行用例
        # run_ids = []  # 已执行的用例id
        # for i in case_ids:
        #     if i in run_ids:
        #         self.reportData[
        #             'error_info'] += f'即将执行的前置步骤: {case_dict[i].name} 已执行过,属于重复前置步骤，请确认'
        #         self.reportData['result'] = False
        #     else:
        #         run_ids.append(i)
        #         apis = CaseApi.objects.filter(Q(case=case_dict[i]) & Q(disabled=False))
        #         for api in apis:
        #             self.run_api(api=api)
        #         if not self.reportData['case_data']:
        #             self.reportData['result'] = False


def run_api(request):
    """运行用例的单个接口"""
    data = save_case(request)
    case_info = json.loads(request.body.decode('utf-8'))
    case = TestCase.objects.get(id=case_info['case_id'])
    run_env = case.web_type + '://' + case.host  # 运行环境
    # 获取版本变量
    v_params = list(
        VersionParamsManage.objects.filter((Q(run_env=run_env) & Q(version=case.version)) | Q(is_share=True)).values())
    v_params = {i['key']: i['value'] for i in v_params}
    report = GenerateReport(version_params=v_params, web_method=case.web_method, host=case.host)
    report.set_testcase(testcase=case)
    report.run_api(testcase=case, api=CaseApi.objects.get(tree_id=int(request.GET.get('api_id'))))
    # 生成用例运行报告
    report.update_report({'case_id': case.id, 'project_id': case.project_id})
    ReportDebugTestcase.objects.create(**report.reportData)
    return data


def run_apis(request):
    """运行用例接口"""
    data = save_case(request)
    case = TestCase.objects.get(id=request.GET.get('case_id'))
    run_env = case.web_method + '://' + case.host  # 运行环境
    # 获取版本变量
    v_params = list(
        VersionParamsManage.objects.filter(
            (Q(run_env=run_env) & Q(version=case.version)) | (Q(is_share=True) & Q(version=case.version))).values())
    v_params = {i['key']: i['value'] for i in v_params}
    report = GenerateReport(version_params=v_params, web_method=case.web_method, host=case.host)
    # 运行用例
    report.set_testcase(testcase=case)
    report.run_case()
    # 生成用例运行报告
    report.update_report({'case_id': case.id, 'project_id': case.project_id, 'params': report.tq})
    ReportDebugTestcase.objects.create(**report.reportData)
    return data


def clear_report(request):
    """清空用例报告"""
    case_id = request.GET.get('case_id')
    ReportDebugTestcase.objects.filter(case_id=case_id).delete()
    return debug_report(request)


def debug_report(request):
    """查询用例报告列表记录"""
    report_list = list(ReportDebugTestcase.objects.filter(case_id=request.GET.get('case_id')).values())
    res = {'data': report_list, 'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=CJsonEncode), content_type='application/json')


def debug_report_detail(request):
    """查询单个用例报告记录详情"""
    data = ReportDebugTestcase.objects.get(id=request.GET.get('id'))
    res = {'id': data.id, 'case_name': data.case_name,
           'data': {'data': eval(data.case_data), 'error_info': data.error_info, 'params': data.params},
           'message': '成功'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')
