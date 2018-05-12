#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from Comments.models import Comments
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

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


class RequestDispatcherView(APIView):
    # 增加
    def post(selfs, request):
        return add_comments(request)

    # 删除
    def delete(self, request):
        return delete_comments(request)

    # 更改状态
    def patch(self, request):
        return alter_comments_status(request)

    # 更改信息
    def put(self, request):
        return alter_comments(request)

    # 获取
    def get(self, request):
        return get_comments(request)


# 获取评论信息
def get_comments(request):
    """/comments/"""
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
        return get_all_comments(request, req_page, page_size)
    elif len(request.GET) - arg_count > 1 or len(request.GET) - arg_count < 0:
        if len(
                request.GET) - arg_count == 3 and 'type' in request.GET.keys() and 'obj' in request.GET.keys() \
                and 'status' in request.GET.keys():
            return get_comments_by_type_obj_status(request, req_page, page_size)
        else:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        if 'id' in request.GET.keys():
            return get_comments_by_id(request)
        elif 'user' in request.GET.keys():
            return get_comments_by_user(request, req_page, page_size)
        elif 'type' in request.GET.keys():
            return get_comments_by_type(request, req_page, page_size)
        if 'obj' in request.GET.keys():
            return get_comments_by_obj(request, req_page, page_size)
        else:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 获取所有的评论信息
def get_all_comments(request, page, page_size):
    """/comments"""
    status, comments = Comments.get_all_comments()
    if status:
        data = []
        page_data = pagination_tool(comments, req_page=page, page_size=page_size)
        comments = page_data['data']
        for item in comments:
            dic = {
                'cid': item.id,
                'user': item.user,
                'o_type': item.o_type,
                'obj': item.obj,
                'content': item.content,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'upvote': item.upvote,
                'deal': item.deal,
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


# 通过id获取评论内容
def get_comments_by_id(request):
    """/comments/{id}"""
    try:
        str_id = request.GET['id']
        cid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, comments = Comments.get_comment_by_id(cid)
        if status:
            data = {
                'cid': comments.id,
                'user': comments.user,
                'o_type': comments.o_type,
                'obj': comments.obj,
                'content': comments.content,
                'date': comments.date.strftime('%Y-%m-%d'),
                'time': comments.time.strftime('%H:%M:%S'),
                'upvote': comments.upvote,
                'deal': comments.deal,
                'status': comments.status
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


# 通过用户ID获取评论内容
def get_comments_by_user(request, page, page_size):
    """/comments/{user}"""
    try:
        str_user = request.GET['user']
        user = int(str_user)
        status, comments = Comments.get_comments_by_user(user=user)
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
            page_data = pagination_tool(comments, req_page=page, page_size=page_size)
            comments = page_data['data']
            for item in comments:
                dic = {
                    'cid': item.id,
                    'user': item.user,
                    'o_type': item.o_type,
                    'obj': item.obj,
                    'content': item.content,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'upvote': item.upvote,
                    'deal': item.deal,
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


# 通过o_type获取评论内容
def get_comments_by_type(request, page, page_size):
    """/comments/{type}"""
    try:
        str_type = request.GET['type']
        typ = int(str_type)
        status, comments = Comments.get_comments_by_type(o_type=typ)
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
            page_data = pagination_tool(comments, req_page=page, page_size=page_size)
            comments = page_data['data']
            for item in comments:
                dic = {
                    'cid': item.id,
                    'user': item.user,
                    'o_type': item.o_type,
                    'obj': item.obj,
                    'content': item.content,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'upvote': item.upvote,
                    'deal': item.deal,
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


# 通过评论对象获取评论内容
def get_comments_by_obj(request, page, page_size):
    """/comments/{type}"""
    try:
        str_obj = request.GET['obj']
        obj = int(str_obj)
        status, comments = Comments.get_comments_by_obj(obj=obj)
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
            page_data = pagination_tool(comments, req_page=page, page_size=page_size)
            comments = page_data['data']
            for item in comments:
                dic = {
                    'cid': item.id,
                    'user': item.user,
                    'o_type': item.o_type,
                    'obj': item.obj,
                    'content': item.content,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'upvote': item.upvote,
                    'deal': item.deal,
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
def get_comments_by_type_obj_status(request, page, page_size):
    """/comments/{status}"""
    try:
        typ = int(request.GET['type'])
        obj = int(request.GET['obj'])
        sta = int(request.GET['status'])
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
        status, comments = Comments.get_comments_by_type_obj_status(typ=typ, obj=obj, status=sta)
        if status:
            data = []
            page_data = pagination_tool(comments, req_page=page, page_size=page_size)
            comments = page_data['data']
            for item in comments:
                dic = {
                    'cid': item.id,
                    'user': item.user,
                    'o_type': item.o_type,
                    'obj': item.obj,
                    'content': item.content,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'upvote': item.upvote,
                    'deal': item.deal,
                    'status': item.status,
                    'comm': get_comment_use_recursion(item.id, 0)
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
def add_comments(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        user = request.POST['user']
        typ = request.POST['type']
        obj = request.POST['obj']
        content = request.POST['content']
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
        sta, cid = Comments.insert(user=user, o_type=typ, obj=obj, content=content, date=date, time=time)
        rtu = {
            'code': 100,
            'status': sta,
            'message': 'success',
            'data': {
                'id': cid
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 删除评论
@csrf_exempt
def delete_comments(request):
    """/comments/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            cid = int(request.data['cid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, comments = Comments.delete_comment_by_id(cid=cid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': comments,
                    'data': {
                        'id': cid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': comments
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


# 更该评论内容
@csrf_exempt
def alter_comments(request):
    """/comments/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    try:
        cid = int(request.data['cid'])
        user = request.data['user']
        typ = request.data['type']
        obj = request.data['obj']
        content = request.data['content']
        date = request.data['date']
        time = request.data['time']
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, message = Comments.update(cid=cid, user=user, o_type=typ, obj=obj, content=content, date=date,
                                       time=time)
        rtu = {
            'code': 100,
            'status': sta,
            'message': message,
            'data': {
                'id': cid
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)



# 更改deal状态
@csrf_exempt
def alter_comments_deal(request):
    """/comments/deal/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            cid = int(request.POST['cid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, comments = Comments.get_comment_by_id(cid=cid)
            if sta:
                if comments.deal == 0:
                    comments.deal = 1
                    sta, message = Comments.update(cid=cid, deal=1)
                else:
                    comments.deal = 0
                    sta, message = comments.update(cid=cid, deal=0)
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': message,
                    'data': {
                        'deal': comments.deal
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': comments
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


# 更改评论状态
@csrf_exempt
def alter_comments_status(request):
    """/comments/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    try:
        cid = int(request.data['cid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, comments = Comments.get_comment_by_id(cid=cid)
        if sta:
            if comments.status == 0:
                comments.status = 1
                sta, message = Comments.update(cid=cid, status=1)
            else:
                comments.status = 0
                sta, message = comments.update(cid=cid, status=0)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
                'data': {
                    'status': comments.status
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': comments
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


def get_comment_use_recursion(cid, deepth):
    sta, comments = Comments.get_comments_by_type_obj_status(typ=COMM_SELF, obj=cid, status=ALLOW)
    comm = []
    for item in comments:
        if deepth > DEEPTH:
            dic = {
                'cid': item.id,
                'user': item.user,
                'o_type': item.o_type,
                'obj': item.obj,
                'content': item.content,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'upvote': item.upvote,
                'deal': item.deal,
                'status': item.status,
                'comm': []
            }
        else:
            dic = {
                'cid': item.id,
                'user': item.user,
                'o_type': item.o_type,
                'obj': item.obj,
                'content': item.content,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'upvote': item.upvote,
                'deal': item.deal,
                'status': item.status,
                'comm': get_comment_use_recursion(item.id, deepth + 1)
            }
        comm.append(dic)
    return comm
