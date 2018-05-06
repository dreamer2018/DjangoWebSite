#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from models import Enrolled
import json
import time as datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小


# 获取报名记录
def get_enrolled(request):
    """/enrolled/"""
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
            return get_all_enrolled(request, req_page, page_size)
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
                return get_enrolled_by_id(request)
            elif 'obj' in request.GET.keys():
                return get_enrolled_by_obj(request, req_page, page_size)
            elif 'status' in request.GET.keys():
                return get_enrolled_by_status(request, req_page, page_size)
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


# 获取所有报名信息
def get_all_enrolled(request, page, page_size):
    """/enrolled"""
    status, enrolled = Enrolled.get_all_enrolled()
    if status:
        data = []
        page_data = pagination_tool(enrolled, req_page=page, page_size=page_size)
        enrolled = page_data['data']
        for item in enrolled:
            dic = {
                'eid': item.id,
                'uid': item.uid,
                'obj': item.obj,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                "status": item.status,
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


# 通过id获取报名信息
def get_enrolled_by_id(request):
    """/enrolled/{id}"""
    try:
        str_id = request.GET['id']
        eid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, enrolled = Enrolled.get_enrolled_by_id(eid)
        if status:
            data = {
                'eid': enrolled.id,
                'uid': enrolled.uid,
                'obj': enrolled.obj,
                'date': enrolled.date.strftime('%Y-%m-%d'),
                'time': enrolled.time.strftime('%H:%M:%S'),
                "status": enrolled.status,
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


# 通过obj获取报名信息
def get_enrolled_by_obj(request, page, page_size):
    """/enrolled/{obj}"""
    try:
        str_obj = request.GET['obj']
        obj = int(str_obj)
        status, enrolled = Enrolled.get_enrolled_by_obj(obj=obj)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid arguments!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
            page_data = pagination_tool(enrolled, req_page=page, page_size=page_size)
            enrolled = page_data['data']
            for item in enrolled:
                dic = {
                    'eid': item.id,
                    'uid': item.uid,
                    'obj': item.obj,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    "status": item.status,
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


# 通过status获取报名信息
def get_enrolled_by_status(request, page, page_size):
    """/enrolled/{status}"""
    try:
        str_status = request.GET['status']
        sta = int(str_status)
        status, enrolled = Enrolled.get_enrolled_by_status(status=sta)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
            page_data = pagination_tool(enrolled, req_page=page, page_size=page_size)
            enrolled = page_data['data']
            for item in enrolled:
                dic = {
                    'eid': item.id,
                    'uid': item.uid,
                    'obj': item.obj,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    "status": item.status,
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


# 增加新的报名用户信息
@csrf_exempt
def add_enrolled(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            obj = int(request.POST['obj'])
            uid = int(request.POST['uid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            date = datetime.strftime('%Y-%m-%d', datetime.localtime(datetime.time()))
            time = datetime.strftime('%H:%M:%S', datetime.localtime(datetime.time()))
            sta, eid = Enrolled.insert(obj=obj, uid=uid, date=date, time=time)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': eid
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


# 更改反馈状态
@csrf_exempt
def alter_enrolled(request):
    """/enrolled/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
            obj = int(request.POST['obj'])
            uid = int(request.POST['uid'])
            date = request.POST['date']
            time = request.POST['time']
            status = None
            if 'status' in request.POST.keys():
                status = int(request.POST['status'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, enrolled = Enrolled.get_enrolled_by_id(eid=eid)
            if sta:
                if status is not None:
                    sta, message = Enrolled.update(eid=eid, obj=obj, uid=uid, date=date, time=time, status=status)
                else:
                    sta, message = Enrolled.update(eid=eid, obj=obj, uid=uid, date=date, time=time)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': enrolled.id
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': enrolled
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


# 更改活动状态
@csrf_exempt
def alter_enrolled_status(request):
    """/events/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, enrolled = Enrolled.get_enrolled_by_id(eid=eid)
            if sta:
                if enrolled.status == 0:
                    enrolled.status = 1
                    sta, message = Enrolled.update(eid=eid, status=1)
                else:
                    enrolled.status = 0
                    sta, message = Enrolled.update(eid=eid, status=0)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': enrolled.status
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': enrolled
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


# 删除报名信息
@csrf_exempt
def delete_enrolled(request):
    """/enrolled/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, enrolled = Enrolled.delete_enrolled_by_id(eid=eid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': enrolled,
                    'data': {
                        'id': eid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': enrolled
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
