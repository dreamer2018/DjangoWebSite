#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from News.models import News
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小


# Create your views here.
class RequestDispatcherView(APIView):
    def __init__(self):
        pass

    # 增加
    def post(selfs, request):
        return add_news(request)

    # 删除
    def delete(self, request):
        return delete_news(request)

    # 更改内容
    def put(self, request):
        return alter_news(request)

    # 更改状态
    def patch(self, request):
        return alter_news_status(request)

    # 获取
    def get(self, request):
        return get_news(request)

# /news/
def get_news(request):
    """/news/"""
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
        return get_all_news(request, req_page, page_size)
    elif len(request.GET) - arg_count > 1 or len(request.GET) - arg_count < 0:
        # 参数错误
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if 'id' in request.GET.keys():
            return get_news_by_id(request)
        elif 'title' in request.GET.keys():
            return get_news_by_title(request, page=req_page, page_size=page_size)
        elif 'status' in request.GET.keys():
            return get_news_by_status(request, page=req_page, page_size=page_size)
        else:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 获取所有的新闻
def get_all_news(request, page, page_size):
    """/news"""
    status, news = News.get_all_news()
    if status:
        data = []
        page_data = pagination_tool(news, req_page=page, page_size=page_size)
        news = page_data['data']
        for item in news:
            dic = {
                'nid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'labels': item.labels,
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


#
# rtu = {
#        'all_count': p.count,  # 所有数量
#        'page_count': p.num_pages,  # 分页数量
#        'page_size': page_size,  # 页面大小
#        'req_page': req_page,  # 请求页
#        'data': req.object_list  # 请求数据
#    }

# 通过id获取新闻
def get_news_by_id(request):
    """/news/{id}"""
    try:
        str_id = request.GET['id']
        nid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, news = News.get_news_by_id(nid)
        if status:
            data = {
                'nid': news.id,
                'title': news.title,
                'content': news.content,
                'origin': news.origin,
                'poster': news.poster,
                'date': news.date.strftime('%Y-%m-%d'),
                'time': news.time.strftime('%H:%M:%S'),
                'labels': news.labels,
                'reader': news.reader,
                'upvote': news.upvote,
                'status': news.status
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


# 通过title获取新闻
def get_news_by_title(request, page, page_size):
    """/news/{title}"""
    # 获取所有News
    title = request.GET['title']
    status, news = News.get_news_by_title(title=title)
    if status:
        data = []
        page_data = pagination_tool(news, req_page=page, page_size=page_size)
        news = page_data['data']
        for item in news:
            dic = {
                'nid': item.id,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'labels': item.labels,
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


# 通过status获取新闻内容
def get_news_by_status(request, page, page_size):
    """/news/{status}"""
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
        status, news = News.get_news_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(news, req_page=page, page_size=page_size)
            news = page_data['data']
            for item in news:
                dic = {
                    'nid': item.id,
                    'title': item.title,
                    'content': item.content,
                    'origin': item.origin,
                    'poster': item.poster,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'labels': item.labels,
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


# 增加新的新闻内容
@csrf_exempt
def add_news(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        title = request.POST['title']
        content = request.POST['content']
        origin = request.POST['origin']
        date = request.POST['date']
        time = request.POST['time']
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
            sta, nid = News.insert(title=title, content=content, origin=origin, date=date, time=time, labels=labels,
                                   poster=poster)
        else:
            sta, nid = News.insert(title=title, content=content, origin=origin, date=date, time=time, labels=labels)
        rtu = {
            'code': 100,
            'status': sta,
            'message': 'success',
            'data': {
                'id': nid
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改新闻内容
@csrf_exempt
def alter_news(request):
    """/news/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        nid = int(request.data['nid'])
        title = request.data['title']
        content = request.data['content']
        origin = request.data['origin']
        date = request.data['date']
        time = request.data['time']
        labels = request.data['labels']
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
            sta, message = News.update(nid=nid, title=title, content=content, origin=origin, date=date, time=time,
                                       labels=labels,
                                       poster=poster)
        else:
            sta, message = News.update(nid=nid, title=title, content=content, origin=origin, date=date, time=time,
                                       labels=labels)
        rtu = {
            'code': 100,
            'status': sta,
            'message': message,
            'data': {
                'id': nid
            }
        }
        js = json.dumps(rtu)
        return HttpResponse(js)



# 更改新闻状态
@csrf_exempt
def alter_news_status(request):
    """/news/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        nid = int(request.data['nid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, new = News.get_news_by_id(nid=nid)
        if sta:
            if new.status == 0:
                new.status = 1
                sta, message = News.update(nid=nid, status=1)
            else:
                new.status = 0
                sta, message = News.update(nid=nid, status=0)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
                'data': {
                    'status': new.status
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': new
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 删除新闻
@csrf_exempt
def delete_news(request):
    """/news/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        nid = int(request.data['nid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, new = News.delete_news_by_id(nid=nid)
        if sta:
            rtu = {
                'code': 100,
                'status': sta,
                'message': new,
                'data': {
                    'id': nid
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': new
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
