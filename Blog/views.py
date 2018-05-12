#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.shortcuts import HttpResponse
from Blog.models import Blog
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import urllib.request as urllib2
from rest_framework.views import APIView

# Create your views here.

# 定义分页宏
REQ_PAGE = 1  # 请求页
PAGE_SIZE = 20  # 页面大小
GET_BLOG_APT = "http://blog.xiyoulinux.org/blogjson"


class RequestDispatcherView(APIView):
    # 获取
    def get(self, request):
        return get_blog(request)

    # 增加
    def post(selfs, request):
        return add_blog(request)

    # 更改状态
    def patch(self, request):
        return alter_blog_status(request)

    # 删除
    def delete(self, request):
        return delete_blog(request)


# /blog/
def get_blog(request):
    """/blog/"""
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
            return get_all_blogs(request, req_page, page_size)
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
                return get_blog_by_id(request)
            elif 'title' in request.GET.keys():
                return get_blog_by_title(request, page=req_page, page_size=page_size)
            elif 'status' in request.GET.keys():
                return get_blog_by_status(request, page=req_page, page_size=page_size)
            else:
                rtu = {
                    'code': 104,
                    'status': False,
                    'message': 'invalid argument',
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        # 请求方法错误
        rtu = {
            'code': 105,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 获取所有的文章
def get_all_blogs(request, page, page_size):
    """/blog"""
    status, blogs = Blog.get_all_blogs()
    if status:
        data = []
        page_data = pagination_tool(blogs, req_page=page, page_size=page_size)
        blog = page_data['data']
        for item in blog:
            dic = {
                'bid': item.id,
                'title': item.title,
                'author': item.author,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'summary': item.summary,
                'url': item.url,
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

# 通过id获取文章
def get_blog_by_id(request):
    """/blog/{id}"""
    try:
        str_id = request.GET['id']
        bid = int(str_id)
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, blog = Blog.get_blog_by_id(bid)
        if status:
            data = {
                'bid': blog.id,
                'title': blog.title,
                'author': blog.author,
                'date': blog.date.strftime('%Y-%m-%d'),
                'time': blog.time.strftime('%H:%M:%S'),
                'summary': blog.summary,
                'url': blog.url,
                'status': blog.status
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


# 通过title获取文章
def get_blog_by_title(request, page, page_size):
    """/news/{title}"""
    # 获取所有Blog
    title = request.GET['title']
    status, blog = Blog.get_blog_by_title(title=title)
    if status:
        data = []
        page_data = pagination_tool(blog, req_page=page, page_size=page_size)
        blog = page_data['data']
        for item in blog:
            dic = {
                'bid': item.id,
                'title': item.title,
                'author': item.author,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'summary': item.summary,
                'url': item.url,
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
def get_blog_by_status(request, page, page_size):
    """/blog/{status}"""
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
        status, blogs = Blog.get_blog_by_status(status=sta)
        if status:
            data = []
            page_data = pagination_tool(blogs, req_page=page, page_size=page_size)
            blog = page_data['data']
            for item in blog:
                dic = {
                    'bid': item.id,
                    'title': item.title,
                    'author': item.author,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'summary': item.summary,
                    'url': item.url,
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


# 增加新的博客内容
@csrf_exempt
def add_blog(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            title = request.POST['title']
            author = request.POST['author']
            date = request.POST['date']
            time = request.POST['time']
            summary = request.POST['summary']
            url = request.POST['url']
        except Exception:
            rtu = {
                'code': 104,
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, bid = Blog.insert(title=title, author=author, date=date, time=time, summary=summary, url=url, status=0)
            rtu = {
                'code': 100,
                'status': sta,
                'message': 'success',
                'data': {
                    'id': bid
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


# 更改文章状态
@csrf_exempt
def alter_blog_status(request):
    """/blog/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    try:
        bid = int(request.data['bid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, blog = Blog.get_blog_by_id(bid=bid)
        if sta:
            if blog.status == 0:
                blog.status = 1
                sta, message = Blog.alter_blog_status(bid=bid, status=1)
            else:
                blog.status = 0
                sta, message = Blog.alter_blog_status(bid=bid, status=0)
            rtu = {
                'code': 100,
                'status': sta,
                'message': message,
                'data': {
                    'status': blog.status
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': blog
            }
            js = json.dumps(rtu)
            return HttpResponse(js)



# 删除新闻
@csrf_exempt
def delete_blog(request):
    """/blog/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    try:
        bid = int(request.data['bid'])
    except Exception:
        rtu = {
            'code': 104,
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        sta, blog = Blog.delete_blog_by_id(bid=bid)
        if sta:
            rtu = {
                'code': 100,
                'status': sta,
                'message': blog,
                'data': {
                    'id': bid
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'code': 106,
                'status': sta,
                'message': blog
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


def get_blog_from_api():
    blogdata = urllib2.urlopen(GET_BLOG_APT)
    if blogdata.code == 200:
        html = blogdata.read()
        html = html.decode('utf-8')
        js = json.loads(html)
        blogs = []
        for i in js:
            title = js[i]['Title']
            author = js[i]['Author']
            summary = js[i]['ArticleDetail']
            url = js[i]['BlogArticleLink']
            dt = js[i]['PubDate']
            date = dt.split()[0]
            time = dt.split()[1]
            blog = {
                'title': title,
                'author': author,
                'date': "20%s" % date.decode('ascii'),
                'time': time.decode('ascii'),
                'summary': summary,
                'url': url
            }
            blogs.append(blog)
        return blogs
    return []


def save_blog_from_api():
    blogs = get_blog_from_api()
    for blog in blogs:
        title = blog['title']
        author = blog['author']
        date = blog['date']
        time = blog['time']
        summary = blog['summary']
        url = blog['url']
        status, blog_info = Blog.get_blog_by_title(title=title, sign=1)
        if len(blog_info) == 0:
            Blog.insert(title=title, author=author, date=date, time=time, summary=summary, url=url, status=1)
