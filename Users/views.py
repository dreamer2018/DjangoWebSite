#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from models import Anonymous, Devuser
import json
from django.views.decorators.csrf import csrf_exempt
from OAuth_Django_SDK import combine_url, GET_USER_INFO_URL
import urllib

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


# 获取匿名用户信息
def get_anonymous(request):
    """/anonymous/"""
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
            return get_all_anonymous(request, req_page, page_size)
        elif len(request.GET) - arg_count > 1 or len(request.GET) - arg_count < 0:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if 'id' in request.GET.keys():
                return get_anonymous_by_id(request)
            elif 'email' in request.GET.keys():
                return get_anonymous_by_email(request, req_page, page_size)
            else:
                rtu = {
                    'code': 104,
                    'status': False,
                    'message': 'invalid argument!',
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


# 获取所有的匿名用户信息
def get_all_anonymous(request, page, page_size):
    """/anonymous"""
    status, anonymous = Anonymous.get_all_anonymous()
    if status:
        data = []
        page_data = pagination_tool(anonymous, req_page=page, page_size=page_size)
        anonymous = page_data['data']
        for item in anonymous:
            dic = {
                'aid': item.id,
                'email': item.email,
                'nickname': item.nickname
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


# 通过id获取匿名用户信息
def get_anonymous_by_id(request):
    """/anonymous/{id}"""
    try:
        str_id = request.GET['id']
        uid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, anonymous = Anonymous.get_anonymous_by_id(uid)
        if status:
            data = {
                'aid': anonymous.id,
                'email': anonymous.email,
                'nickname': anonymous.nickname
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


# 通过email获取匿名用户
def get_anonymous_by_email(request, page, page_size):
    """/anonymous/{content}"""
    email = request.GET['email']
    status, anonymous = Anonymous.get_anonymous_by_email(email=email)
    if status:
        data = []
        page_data = pagination_tool(anonymous, req_page=page, page_size=page_size)
        anonymous = page_data['data']
        for item in anonymous:
            dic = {
                'aid': item.id,
                'email': item.email,
                'nickname': item.nickname
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


# 增加新的匿名用户信息
@csrf_exempt
def add_anonymous(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            email = request.POST['email']
            nickname = request.POST['nickname']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, uid = Anonymous.insert(nickname=nickname, email=email)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': uid
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


# 删除匿名用户信息
@csrf_exempt
def delete_anonymous(request):
    """/anonymous/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            aid = int(request.POST['aid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, anonymous = Anonymous.delete_anonymous_by_id(uid=aid)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': anonymous,
                    'data': {
                        'id': aid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': anonymous
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


# 获取开发者信息
def get_devuser(request):
    """/devuser/"""
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
            return get_all_devuser(request, req_page, page_size)
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
                return get_devuser_by_id(request)
            elif 'pid' in request.GET.keys():
                return get_devuser_by_pid(request, req_page, page_size)
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


# 获取所有开发者信息
def get_all_devuser(request, page, page_size):
    """/devuser"""
    status, devuser = Devuser.get_all_devuser()
    if status:
        data = []
        page_data = pagination_tool(devuser, req_page=page, page_size=page_size)
        devuser = page_data['data']
        for item in devuser:
            dic = {
                'did': item.id,
                'uid': item.uid,
                'pid': item.pid
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


# 通过id获取开发者信息
def get_devuser_by_id(request):
    """/devuser/{id}"""
    try:
        str_id = request.GET['id']
        uid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, devuser = Devuser.get_devuser_by_id(uid=uid)
        if status:
            data = {
                'did': devuser.id,
                'uid': devuser.uid,
                'pid': devuser.pid
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


# 通过obj获取开发者信息
def get_devuser_by_pid(request, page, page_size):
    """/devuser/{obj}"""
    try:
        str_pid = request.GET['pid']
        pid = int(str_pid)
        status, devuser = Devuser.get_devuser_by_pid(pid=pid)
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
            page_data = pagination_tool(devuser, req_page=page, page_size=page_size)
            devuser = page_data['data']
            for item in devuser:
                dic = {
                    'did': item.id,
                    'uid': item.uid,
                    'pid': item.pid
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


# 增加新的开发者信息
@csrf_exempt
def add_devuser(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            uid = int(request.POST['uid'])
            pid = int(request.POST['pid'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, uid = Devuser.insert(uid=uid, pid=pid)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': uid
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


# 删除开发者
@csrf_exempt
def delete_devuser(request):
    """/devuser/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            did = int(request.POST['did'])
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, devuser = Devuser.delete_devuser_by_id(uid=did)
            if sta:
                rtu = {
                    'code': 100,
                    'status': sta,
                    'message': devuser,
                    'data': {
                        'id': did
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'code': 106,
                    'status': sta,
                    'message': devuser
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


# 获取用户信息
def get_current_user_info(request):
    if 'login' in request.session.keys() and request.session['login']:
        access_token = request.session['access_token']
        data = {
            'access_token': access_token
        }
        url = combine_url(GET_USER_INFO_URL, data)
        params = urllib.unquote(url)
        try:
            response = urllib.urlopen(params)
        except IOError:
            rtu = {
                'code': 101,
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 100,
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'code': 107,
            'status': False,
            'message': 'user not login!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 获取所有用户信息
def get_all_user_info(request):
    if 'login' in request.session.keys() and request.session['login']:
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
        access_token = request.session['access_token']
        url = "https://api.xiyoulinux.org/users?page=%d&per_page=%d&access_token=%s" % (
            req_page, page_size, access_token)
        params = urllib.unquote(url)
        try:
            response = urllib.urlopen(params)
        except IOError:
            rtu = {
                'code': 101,
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 100,
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'code': 107,
            'status': False,
            'message': 'user not login!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 获取所有用户信息
def get_user_by_id(request):
    if 'id' not in request.GET.keys():
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    try:
        int(request.GET['id'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    if 'login' in request.session.keys() and request.session['login']:
        access_token = request.session['access_token']
        url = "https://api.xiyoulinux.org/users/%s?access_token=%s" % (request.GET['id'], access_token)
        params = urllib.unquote(url)
        try:
            response = urllib.urlopen(params)
        except IOError:
            rtu = {
                'code': 101,
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 100,
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'code': 107,
            'status': False,
            'message': 'user not login!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 判断用户是否登录
def is_login(request):
    if 'login' in request.session.keys() and request.session['login']:
        access_token = request.session['access_token']
        data = {
            'access_token': access_token
        }
        url = combine_url(GET_USER_INFO_URL, data)
        params = urllib.unquote(url)
        try:
            urllib.urlopen(params)
        except IOError, e:
            request.session['login'] = False
            return False, 'login out of time!'
        else:
            return True, 'login success!'
    else:
        return False, 'not login!'

# 403
def permission_denied(request):
    rtu = {
        'code': 107,
        'status': False,
        'message': 'Forbidden',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 404
def page_not_found(request):
    rtu = {
        'code': 102,
        'status': False,
        'message': 'page not found',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 500
def server_error(request):
    rtu = {
        'code': 103,
        'status': False,
        'message': 'server error!',
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
