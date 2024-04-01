import json
import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import *

from .models import *


logger = logging.getLogger('django')


# Create your views here.
def login_page(request, message=''):
    return render(request, template_name='login.html', context={'message': message})


@login_required()
def index(request):
    return render(request, 'index.html')


def login_auth(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth.login(request, user)
            res = {'login_auth': True, 'message': '成功'}
        else:
            res = {'login_auth': False, 'message': '账号未激活！'}
    else:
        res = {'login_auth': False, 'message': '账号或密码错误！'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


@api_view(['GET', 'POST'])
def base_user(request):
    def get_users():
        """返回人员数据列表"""
        all_info = UserInfo.objects.filter(user__in=(User.objects.filter(is_active=1))).all()
        user_data = UserinfoSerializer(all_info, many=True)
        return Response(user_data.data)

    def get_user():
        """返回单个人员数据信息"""
        return Response(UserinfoSerializer(UserInfo.objects.filter(user_id=request.data['id'])).data)

    if request.method == 'GET':
        if 'id' in request.data:
            return get_user()
        else:
            return get_users()

    if request.method == 'POST':
        post_data = request.data
        if 'id' in post_data:
            # 删除
            if 'is_delete' in post_data:
                user = User.objects.get(id=post_data['id'])
                user.is_active = 0
                user.save()
        else:
            # 新增
            base_info = post_data["base_info"]
            user_info = post_data["user_info"]
            extra_fields = {'first_name': post_data["user_info"]['name']}
            b_user = User.objects.create_user(username=base_info['username'], password=base_info['username'],
                                              **extra_fields)

            user_info['user'] = b_user
            user_info_serializer = UserinfoSerializer(data=user_info, many=False)
            try:
                user_info_serializer.is_valid(raise_exception=True)
                user_info_serializer.save(user=b_user)  # 添加新增的user对象（关联的用户表）
            except Exception as e:
                raise user_info_serializer.errors
        return get_users()


def user_detail(request):
    """获取用户详情信息"""
    fields = ['id', 'is_superuser', 'first_name', 'is_active']
    user_info = list(User.objects.filter(id=request.user.id).values(*fields))[0]
    return HttpResponse(json.dumps(user_info, ensure_ascii=False), content_type='application/json')


@api_view(['GET', 'POST'])
def power_list(request):
    def get_powers():
        """获取权限列表"""
        powers = PowerConfSerializer(PowerConf.objects.all(), many=True)
        return Response(powers.data)

    def add_or_delete_power():
        """新增或删除权限列表"""
        data = request.data
        if 'id' in data:
            PowerConf.objects.get(id=data['id']).delete()
        else:
            power_serializer = PowerConfSerializer(data=data)
            if power_serializer.is_valid():
                power_serializer.save()
        return get_powers()

    if request.method == "GET":
        return get_powers()

    elif request.method == 'POST':
        return add_or_delete_power()


def logout(request):
    """注销退出"""
    auth.logout(request)
    res = {'message': '成功', 'type': 'success'}
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


# @login_required()
def static_data(request):
    """返回首页概览信息"""
    tj_data = {
        "project_overflow": {
            "project_num": 10,
            "case_num": 1000,
            "api_num": 100,
        },
        "person_contribution": {
            "project_percent": 10,
            "api_percent": 20,
            "case_percent": 30,
            "monitor_percent": 40,
        },
        "last_run_info": {
            "api_pass_percent": 10,
            "case_pass_percent": 20,
            "case_fail_percent": 30,
        },
        "notice_info": [],
    }
    notice_fields = ['notice_id', 'content', 'create_date']
    info = list(PublicNotice.objects.filter(expiration_date__gte=datetime.now().date()).
                order_by('-expiration_date').values(*notice_fields))
    tj_data['notice_info'] = info
    for i in range(len(info)):
        info[i]['create_date'] = info[i]['create_date'].strftime('%Y-%m-%d')
    return HttpResponse(json.dumps(tj_data, ensure_ascii=False), content_type='application/json')


def realtime_data(request):
    real_time_info = {
        "api_total_nums": 100,
        "no_read_message_nums": 200,
        "run_case_times": 500,
        "import_api_times": 600
    }
    return HttpResponse(json.dumps(real_time_info), content_type='application/json')


def public_notice_list(request):
    result = {"data": [], 'message': '成功', 'status': 200}
    res = list(PublicNotice.objects.all().values())
    for i in res:
        tmp = dict()
        tmp['create_date'] = i['create_date'].strftime('%Y-%m-%d')
        tmp["expiration_date"] = i["expiration_date"].strftime('%Y-%m-%d')
        tmp['content'] = i['content']
        tmp['notice_id'] = i['notice_id']
        result['data'].append(tmp)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def public_notice_add(request):
    request.get_full_path()
    data = json.loads(request.body.decode('utf-8'))
    PublicNotice.objects.create(**data)
    return public_notice_list(request)


def public_notice_delete(request):
    notice_id = request.GET.get('notice_id')
    PublicNotice.objects.filter(notice_id=notice_id).delete()
    return public_notice_list(request)
