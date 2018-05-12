#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from Projects.models import Projects
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
# Create your views here.

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小


# Create your views here.
class RequestDispatcherView(APIView):
    # 增加
    def post(selfs, request):
        return add_projects(request)

    # 删除
    def delete(self, request):
        return delete_projects(request)

    # 更改内容
    def put(self, request):
        return alter_projects(request)

    # 更改状态
    def patch(self, request):
        return alter_projects_status(request)

    # 获取
    def get(self, request):
        return get_projects(request)


# 获取项目信息
def get_projects(request):
    """/projects/"""
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
        return get_all_projects(request, page=req_page, page_size=page_size)
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
            return get_projects_by_id(request)
        elif 'title' in request.GET.keys():
            return get_projects_by_title(request, page=req_page, page_size=page_size)
        elif 'status' in request.GET.keys():
            return get_projects_by_status(request, page=req_page, page_size=page_size)
        else:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 获取所有的项目信息
def get_all_projects(request, page, page_size):
    """/projects"""
    status, projects = Projects.get_all_projects()
    if status:
        data = []
        page_data = pagination_tool(projects, req_page=page, page_size=page_size)
        projects = page_data['data']
        for item in projects:
            dic = {
                'pid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'author': item.author,
                'reader': item.reader,
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


# 通过id获取项目内容
def get_projects_by_id(request):
    """/projects/{id}"""
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
        status, projects = Projects.get_project_by_id(pid)
        if status:
            data = {
                'pid': projects.id,
                'title': projects.title,
                'content': projects.content,
                'origin': projects.origin,
                'poster': projects.poster,
                'link': projects.link,
                'date': projects.date.strftime('%Y-%m-%d'),
                'time': projects.time.strftime('%H:%M:%S'),
                'author': projects.author,
                'reader': projects.reader,
                'upvote': projects.upvote,
                'status': projects.status
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


# 通过title获取项目内容
def get_projects_by_title(request, page, page_size):
    """/projects/{title}"""
    title = request.GET['title']
    status, projects = Projects.get_projects_by_title(title=title)
    if status:
        data = []
        page_data = pagination_tool(projects, req_page=page, page_size=page_size)
        projects = page_data['data']
        for item in projects:
            dic = {
                'pid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'author': item.author,
                'reader': item.reader,
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


# 通过status获取项目内容
def get_projects_by_status(request, page, page_size):
    """/projects/{status}"""
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
        status, projects = Projects.get_projects_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(projects, req_page=page, page_size=page_size)
            projects = page_data['data']
            for item in projects:
                dic = {
                    'pid': item.id,
                    'title': item.title,
                    'content': item.content,
                    'origin': item.origin,
                    'poster': item.poster,
                    'link': item.link,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'author': item.author,
                    'reader': item.reader,
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


# 增加新的项目
@csrf_exempt
def add_projects(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        title = request.POST['title']
        content = request.POST['content']
        origin = request.POST['origin']
        link = request.POST['link']
        date = request.POST['date']
        time = request.POST['time']
        author = request.POST['author']
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
            sta, pid = Projects.insert(title=title, content=content, origin=origin, link=link, date=date,
                                       time=time, author=author, poster=poster)
        else:
            sta, pid = Projects.insert(title=title, content=content, origin=origin, link=link, date=date,
                                       time=time, author=author)
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


# 更改项目内容
@csrf_exempt
def alter_projects(request):
    """/projects/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        pid = int(request.data['pid'])
        title = request.data['title']
        content = request.data['content']
        origin = request.data['origin']
        link = request.data['link']
        date = request.data['date']
        time = request.data['time']
        author = request.data['author']
        poster = None
        if 'poster' in request.data.keys():
            poster = request.data['poster']
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
            sta, message = Projects.update(pid=pid, title=title, content=content, origin=origin, link=link,
                                           date=date, time=time, poster=poster, author=author)
        else:
            sta, message = Projects.update(pid=pid, title=title, content=content, origin=origin, link=link,
                                           date=date, time=time, author=author)
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

# 更改项目状态
@csrf_exempt
def alter_projects_status(request):
    """/projects/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        pid = int(request.data['pid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, projects = Projects.get_project_by_id(pid=pid)
        if sta:
            if projects.status == 0:
                projects.status = 1
                sta, message = projects.update(pid=pid, status=1)
            else:
                projects.status = 0
                sta, message = projects.update(pid=pid, status=0)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
                'data': {
                    'status': projects.status
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': projects
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 删除新闻
@csrf_exempt
def delete_projects(request):
    """/projects/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        pid = int(request.data['pid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, projects = Projects.delete_project_by_id(pid=pid)
        if sta:
            rtu = {
                'code': 100,
                'status': sta,
                'message': projects,
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
                'message': projects
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
