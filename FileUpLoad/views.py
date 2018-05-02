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

# Create your views here.


@csrf_exempt
def upload(request):
    if request.method == "POST":
        filename = handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        host = request.get_host()
        rtu = {
            'code': 100,
            'status': True,
            'message': 'success',
            'data': {
                'path': "%s%s%s" % (host, settings.MEDIA_URL, filename)
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中


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
