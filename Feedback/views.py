#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from models import Feedback
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小


# 获取反馈信息
def get_feedback(request):
    """/feedback/"""
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
            return get_all_feedback(request, page=req_page, page_size=page_size)
        elif len(request.GET) - arg_count > 1 or len(request.GET) - arg_count < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_feedback_by_id(request)
            elif 'content' in request.GET.keys():
                return get_feedback_by_content(request, page=req_page, page_size=page_size)
            elif 'status' in request.GET.keys():
                return get_feedback_by_status(request, page=req_page, page_size=page_size)
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


# 获取所有的反馈信息
def get_all_feedback(request, page, page_size):
    """/feedback"""
    status, feedback = Feedback.get_all_feedback()
    if status:
        data = []
        page_data = pagination_tool(feedback, req_page=page, page_size=page_size)
        feedback = page_data['data']
        for item in feedback:
            dic = {
                'fid': item.id,
                'content': item.content,
                'email': item.email,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
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


# 通过id获取反馈内容
def get_feedback_by_id(request):
    """/feedback/{id}"""
    try:
        str_id = request.GET['id']
        fid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, feedback = Feedback.get_feedback_by_id(fid)
        if status:
            data = {
                'pid': feedback.id,
                'content': feedback.content,
                'email': feedback.email,
                'date': feedback.date.strftime('%Y-%m-%d'),
                'time': feedback.time.strftime('%H:%M:%S'),
                'status': feedback.status
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


# 通过content获取反馈内容
def get_feedback_by_content(request, page, page_size):
    """/feedback/{content}"""
    content = request.GET['content']
    status, feedback = Feedback.get_feedback_by_content(content=content)
    if status:
        data = []
        page_data = pagination_tool(feedback, req_page=page, page_size=page_size)
        feedback = page_data['data']
        for item in feedback:
            dic = {
                'pid': item.id,
                'content': item.content,
                'email': item.email,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
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


# 通过status获取反馈内容
def get_feedback_by_status(request, page, page_size):
    """/feedback/{status}"""
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
        status, feedback = Feedback.get_feedback_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(feedback, req_page=page, page_size=page_size)
            feedback = page_data['data']
            for item in feedback:
                dic = {
                    'pid': item.id,
                    'content': item.content,
                    'email': item.email,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
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


# 增加新的反馈
@csrf_exempt
def add_feedback(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            content = request.POST['content']
            email = request.POST['email']
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
            sta, fid = Feedback.insert(content=content, email=email, date=date, time=time)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': fid
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
def alter_feedback_status(request):
    """/feedback/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            fid = int(request.POST['fid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, feedback = Feedback.get_feedback_by_id(fid=fid)
            if sta:
                if feedback.status == 0:
                    feedback.status = 1
                    sta, message = Feedback.update(fid=fid, status=1)
                else:
                    feedback.status = 0
                    sta, message = Feedback.update(fid=fid, status=0)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': feedback.status
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': feedback
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


# 删除反馈
@csrf_exempt
def delete_feedback(request):
    """/feedback/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            fid = int(request.POST['fid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, feedback = Feedback.delete_feedback_by_id(fid=fid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': feedback,
                    'data': {
                        'id': fid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': feedback
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
