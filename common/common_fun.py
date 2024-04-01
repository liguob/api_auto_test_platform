# -*- coding: utf-8 -*-
"""
============================
@Time   :2023/3/1 23:02
@Author :李国彬
============================
"""
import json
import datetime
from django.http import HttpResponse


def json_http_response(data: dict):
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


class CJsonEncode(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif obj is None:
            return ''
        else:
            return json.JSONEncoder.default(self, obj)
