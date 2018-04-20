#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from models import Events
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# 定义禁用与启用
ALLOW = 1
FORBID = 0

# 定义最大递归深度
DEEPTH = 20

# 定义一些评论对象的宏
COMM_NEWS = 0
COMM_EVENTS = 1
COMM_PICTURES = 2
COMM_PROJECTS = 3
COMM_SELF = 4

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小


# Create your views here.

# 获取活动信息
def get_events(request):
    """/events/"""
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
            return get_all_events(request, page=req_page, page_size=page_size)
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
                return get_events_by_id(request)
            elif 'title' in request.GET.keys():
                return get_events_by_title(request, page=req_page, page_size=page_size)
            elif 'status' in request.GET.keys():
                return get_events_by_status(request, page=req_page, page_size=page_size)
            else:
                rtu = {
                    'code': 104,
                    'status': False,
                    'message': 'invalid argument',
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    rtu = {
        'code': 104,
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的新闻
def get_all_events(request, page, page_size):
    """/events"""
    status, events = Events.get_all_events()
    if status:
        data = []
        page_data = pagination_tool(events, req_page=page, page_size=page_size)
        events = page_data['data']
        for item in events:
            dic = {
                'eid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'address': item.address,
                'labels': item.labels,
                'reader': item.reader,
                'upvote': item.upvote,
                'enroll': item.enroll,
                'status': item.status
            }
            data.append(dic)
        rtu = {
            'code': 200,
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


# 通过id获取活动内容
def get_events_by_id(request):
    """/events/{id}"""
    try:
        str_id = request.GET['id']
        eid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, events = Events.get_events_by_id(eid)
        if status:
            data = {
                'eid': events.id,
                'title': events.title,
                'content': events.content,
                'origin': events.origin,
                'poster': events.poster,
                'date': events.date.strftime('%Y-%m-%d'),
                'time': events.time.strftime('%H:%M:%S'),
                'address': events.address,
                'labels': events.labels,
                'reader': events.reader,
                'upvote': events.upvote,
                'enroll': events.enroll,
                'status': events.status
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


# 通过title获取活动内容
def get_events_by_title(request, page, page_size):
    """/events/{title}"""
    title = request.GET['title']
    status, events = Events.get_events_by_title(title=title)
    if status:
        data = []
        page_data = pagination_tool(events, req_page=page, page_size=page_size)
        events = page_data['data']
        for item in events:
            dic = {
                'eid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'address': item.address,
                'labels': item.labels,
                'reader': item.reader,
                'upvote': item.upvote,
                'enroll': item.enroll,
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


# 通过status获取活动内容
def get_events_by_status(request, page, page_size):
    """/events/{status}"""
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
        status, events = Events.get_events_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(events, req_page=page, page_size=page_size)
            events = page_data['data']
            for item in events:
                dic = {
                    'eid': item.id,
                    'title': item.title,
                    'content': item.content,
                    'origin': item.origin,
                    'poster': item.poster,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'address': item.address,
                    'labels': item.labels,
                    'reader': item.reader,
                    'upvote': item.upvote,
                    'enroll': item.enroll,
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


# 增加新的新闻内容
@csrf_exempt
def add_events(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            origin = request.POST['origin']
            date = request.POST['date']
            time = request.POST['time']
            address = request.POST['address']
            labels = request.POST['labels']
            poster = None
            if 'poster' in request.POST.keys():
                poster = request.POST['poster']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, eid = Events.insert(title=title, content=content, origin=origin, date=date, time=time,
                                         labels=labels, address=address, poster=poster)
            else:
                sta, eid = Events.insert(title=title, content=content, origin=origin, date=date, time=time,
                                         address=address, labels=labels)
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


# 更改活动内容
@csrf_exempt
def alter_events(request):
    """/events/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
            title = request.POST['title']
            content = request.POST['content']
            origin = request.POST['origin']
            date = request.POST['date']
            time = request.POST['time']
            labels = request.POST['labels']
            address = request.POST['address']
            poster = None
            if 'poster' in request.POST.keys():
                poster = request.POST['poster']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, message = Events.update(eid=eid, title=title, content=content, origin=origin, date=date,
                                             time=time, labels=labels, address=address, poster=poster)
            else:
                sta, message = Events.update(eid=eid, title=title, content=content, origin=origin, date=date,
                                             time=time, address=address, labels=labels)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
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


# 更改活动状态
@csrf_exempt
def alter_events_status(request):
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
            sta, events = Events.get_events_by_id(eid=eid)
            if sta:
                if events.status == 0:
                    events.status = 1
                    sta, message = Events.update(eid=eid, status=1)
                else:
                    events.status = 0
                    sta, message = Events.update(eid=eid, status=0)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': events.status
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': events
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


# 删除活动
@csrf_exempt
def delete_events(request):
    """/events/delete/"""
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
            sta, events = Events.delete_events_by_id(eid=eid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': events,
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
                    'message': events
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
