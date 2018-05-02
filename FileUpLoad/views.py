#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/5/2.
"""


from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
# Create your views here.


@csrf_exempt
def upload(request):
    if request.method == "POST":
        handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        return HttpResponse('Successful')  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中


def handle_upload_file(file, filename):
    path = './'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
