#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/5/2.
"""

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time
import json
from django.conf import settings
from rest_framework.views import APIView


# Create your views here.
class RequestDispatcherView(APIView):
    # 增加
    def post(selfs, request):
        return upload(request)


@csrf_exempt
def upload(request):
    if request.method == "POST":
        filename = handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        rtu = {
            'code': 100,
            'status': True,
            'message': 'success',
            'data': {
                'url': "%s%s" % (settings.MEDIA_URL, filename)
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中
    else:
        # 请求方法错误
        rtu = {
            'code': 105,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


def handle_upload_file(file_data, file_name):
    extension = os.path.splitext(file_name)[1]
    filename = "%d%s" % (int(round(time.time()*1000)), extension)
    path = settings.MEDIA_ROOT  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = path + '/' + filename
    with open(full_path, 'wb+') as destination:
        for chunk in file_data.chunks():
            destination.write(chunk)
    return filename
