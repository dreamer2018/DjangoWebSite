#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from models import Pictures
import json
from django.views.decorators.csrf import csrf_exempt

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小

# Create your views here.


# 获取图片信息
def get_pictures(request):
    """/pictures/"""
    if request.method == 'GET':
        arg_count = 0
        req_page = REQ_PAGE
        page_size = PAGE_SIZE

        try:
            if 'page' in request.GET.keys():
                req_page = int(request.GET['page'])
                arg_count += 1
            if 'page_size' in request.GET.keys():
                page_size = int(request.GET['page_size'])
                arg_count += 1
        except Exception:
            # 参数错误
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid arguments!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)

        if len(request.GET) - arg_count == 0:
            return get_all_pictures(request, req_page, page_size)
        elif len(request.GET) - arg_count > 1 or len(request.GET) - arg_count < 0:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if 'id' in request.GET.keys():
                return get_pictures_by_id(request)
            elif 'content' in request.GET.keys():
                return get_pictures_by_content(request, req_page, page_size)
            elif 'status' in request.GET.keys():
                return get_pictures_by_status(request, req_page, page_size)
            else:
                rtu = {
                    'code': 104,
                    'status': False,
                    'message': 'invalid argument',
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    rtu = {
        'code': 105,
        'status': False,
        'message': 'method error!',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的图片信息
def get_all_pictures(request, page, page_size):
    """/pictures"""
    status, pictures = Pictures.get_all_pictures()
    if status:
        data = []
        page_data = pagination_tool(pictures, req_page=page, page_size=page_size)
        pictures = page_data['data']
        for item in pictures:
            dic = {
                'pid': item.id,
                'content': item.content,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'upvote': item.upvote,
                'status': item.status
            }
            data.append(dic)
        rtu = {
            'code': 100,
            'status': True,
            'message': 'success',
            'all_count': page_data['all_count'],
            'page_size': page_data['page_size'],
            'page_count': page_data['page_count'],
            'curr_page': page_data['req_page'],
            'data': data
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        rtu = {
            'code': 106,
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过id获取图片内容
def get_pictures_by_id(request):
    """/pictures/{id}"""
    try:
        str_id = request.GET['id']
        pid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, pictures = Pictures.get_picture_by_id(pid)
        if status:
            data = {
                'pid': pictures.id,
                'content': pictures.content,
                'link': pictures.link,
                'date': pictures.date.strftime('%Y-%m-%d'),
                'time': pictures.time.strftime('%H:%M:%S'),
                'upvote': pictures.upvote,
                'status': pictures.status
            }
            rtu = {
                'code': 100,
                'status': True,
                'message': 'success',
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        rtu = {
            'code': 106,
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过content获取图片内容
def get_pictures_by_content(request, page, page_size):
    """/pictures/{content}"""
    content = request.GET['content']
    status, pictures = Pictures.get_pictures_by_content(content=content)
    if status:
        data = []
        page_data = pagination_tool(pictures, req_page=page, page_size=page_size)
        pictures = page_data['data']
        for item in pictures:
            dic = {
                'pid': item.id,
                'content': item.content,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'upvote': item.upvote,
                'status': item.status
            }
            data.append(dic)
        rtu = {
            'code': 100,
            'status': True,
            'message': 'success',
            'all_count': page_data['all_count'],
            'page_size': page_data['page_size'],
            'page_count': page_data['page_count'],
            'curr_page': page_data['req_page'],
            'data': data
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        rtu = {
            'code': 106,
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过status获取图片内容
def get_pictures_by_status(request, page, page_size):
    """/pictures/{status}"""
    try:
        str_status = request.GET['status']
        sta = int(str_status)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        # 当status 为 0 时，监测是否登陆
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, pictures = Pictures.get_pictures_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(pictures, req_page=page, page_size=page_size)
            pictures = page_data['data']
            for item in pictures:
                dic = {
                    'pid': item.id,
                    'content': item.content,
                    'link': item.link,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'upvote': item.upvote,
                    'status': item.status
                }
                data.append(dic)
            rtu = {
                'code': 100,
                'status': True,
                'message': 'success',
                'all_count': page_data['all_count'],
                'page_size': page_data['page_size'],
                'page_count': page_data['page_count'],
                'curr_page': page_data['req_page'],
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 增加新的图片
@csrf_exempt
def add_pictures(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            content = request.POST['content']
            link = request.POST['link']
            date = request.POST['date']
            time = request.POST['time']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, pid = Pictures.insert(content=content, link=link, date=date, time=time)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': pid
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'code': 105,
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改图片内容
@csrf_exempt
def alter_pictures(request):
    """/pictures/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
            content = request.POST['content']
            link = request.POST['link']
            date = request.POST['date']
            time = request.POST['time']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, message = Pictures.update(pid=pid, content=content, link=link, date=date, time=time)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
                'data': {
                    'id': pid
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'code': 105,
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改图片状态
@csrf_exempt
def alter_pictures_status(request):
    """/pictures/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, picture = Pictures.get_picture_by_id(pid=pid)
            if sta:
                if picture.status == 0:
                    picture.status = 1
                    sta, message = Pictures.update(pid=pid, status=1)
                else:
                    picture.status = 0
                    sta, message = Pictures.update(pid=pid, status=0)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': picture.status
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': picture
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'code': 105,
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 删除图片
@csrf_exempt
def delete_pictures(request):
    """/pictures/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, pictures = Pictures.delete_picture_by_id(pid=pid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': pictures,
                    'data': {
                        'id': pid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': pictures
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'code': 105,
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 判断用户是否登录


def pagination_tool(data, req_page, page_size):
    if page_size <= 0:  # 页面大小小于0，设置页面大小为1
        page_size = 1
    p = Paginator(data, page_size)

    if p.num_pages < req_page:  # 如果请求页面大于最大页面，设置请求页面为最大页面
        req_page = p.num_pages
    req = p.page(req_page)

    rtu = {
        'all_count': p.count,  # 所有数量
        'page_count': p.num_pages,  # 分页数量
        'page_size': page_size,  # 页面大小
        'req_page': req_page,  # 请求页
        'data': req.object_list  # 请求数据
    }
    return rtu
