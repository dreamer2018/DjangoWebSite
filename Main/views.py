#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from models import Anonymous, Events, News, Projects, Pictures, Feedback, Comments
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def test(request):
    anonymous = Anonymous()
    # anonymous.insert("zhoupan", "zhoupans_mail@163.com")
    # status, an = anonymous.get_anonymous_by_id(2)

    # Events.insert(title="第十四届软件自由日", content="第十四届软件自由日（西邮站）圆满落下帷幕", origin="第十四届软件自由日（西邮站）圆满落下帷幕",
    #              date="2017-11-10", time="16:20:00",
    #              address="西安邮电大学", labels="SFD,自由软件", poster="https://www.baidu.com/img/bd_logo1.png")
    # status, event = Events.get_events_by_id(1)

    # Feedback.insert(email="zp@qq.com", content="你好！", date="2017-11-10", time="20:00:00")
    # status, fb = Feedback.get_feedback_by_id(1)
    # return HttpResponse(fb.email)

    # News.insert(title="第十四届软件自由日", content="第十四届软件自由日（西邮站）圆满落下帷幕", origin="第十四届软件自由日（西邮站）圆满落下帷幕",
    #             date="2017-11-10", time="16:20:00", labels="SFD,自由软件",
    #             poster="https://www.baidu.com/img/bd_logo1.png")
    # status, new = News.get_news_by_id(1)

    return HttpResponse(len(request.GET))


# /news/
def get_news(request):
    """/news/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_news(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_news_by_id(request)
            if 'title' in request.GET.keys():
                return get_news_by_title(request)
            if 'status' in request.GET.keys():
                return get_news_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的新闻
def get_all_news(request):
    """/news"""
    status, news = News.get_all_news()
    if status:
        data = []
        for item in news:
            dic = {
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
            'status': True,
            'message': 'success',
            'total_count': len(news),
            'data': data
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过id获取新闻
def get_news_by_id(request):
    """/news/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, news = News.get_news_by_id(id)
        if status:
            data = {
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
                'status': True,
                'message': 'success',
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        rtu = {
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过title获取新闻
def get_news_by_title(request):
    """/news/{title}"""
    # 获取所有News
    title = request.GET['title']
    status, news = News.get_news_by_title(title=title)
    if status:
        data = []
        for item in news:
            dic = {
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
            'status': True,
            'message': 'success',
            'total_count': len(news),
            'data': data
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'not found!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 通过status获取新闻内容
def get_news_by_status(request):
    """/news/{status}"""
    try:
        str_status = request.GET['status']
        sta = int(str_status)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        # 当status 为 0 时，监测是否登陆
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
        status, news = News.get_news_by_status(status=sta)
        if status:
            data = []
            for item in news:
                dic = {
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
                'status': True,
                'message': 'success',
                'total_count': len(news),
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 增加新的新闻内容
@csrf_exempt
def add_news(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, id = News.insert(title=title, content=content, origin=origin, date=date, time=time, labels=labels,
                                      poster=poster)
            else:
                sta, id = News.insert(title=title, content=content, origin=origin, date=date, time=time, labels=labels)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'id': id
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)

    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改新闻内容
@csrf_exempt
def alter_news(request):
    """/news/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            nid = int(request.POST['nid'])
            title = request.POST['title']
            content = request.POST['content']
            origin = request.POST['origin']
            date = request.POST['date']
            time = request.POST['time']
            labels = request.POST['labels']
            poster = None
            if 'poster' in request.POST.keys():
                poster = request.POST['poster']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, message = News.update(id=nid, title=title, content=content, origin=origin, date=date, time=time,
                                           labels=labels,
                                           poster=poster)
            else:
                sta, message = News.update(id=nid, title=title, content=content, origin=origin, date=date, time=time,
                                           labels=labels)
            rtu = {
                'status': sta,
                'message': message,
                'data': {
                    'id': nid
                }
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改新闻状态
@csrf_exempt
def alter_status(request):
    """/news/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            nid = int(request.POST['nid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, new = News.get_news_by_id(id=nid)
            if sta:
                if new.status == 0:
                    sta, message = News.update(id=nid, status=1)
                else:
                    sta, message = News.update(id=nid, status=0)
                rtu = {
                    'status': sta,
                    'message': message,
                    'data': {
                        'id': nid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': new
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 删除新闻
@csrf_exempt
def delete_news(request):
    """/news/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            nid = int(request.POST['nid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, new = News.delete_news_by_id(id=nid)
            if sta:
                rtu = {
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
                    'status': sta,
                    'message': new
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 判断用户是否登录
def is_login(request):
    if 'login' in request.session.keys() and request.session['login']:
        return True, request.session['user']
    else:
        return False, None
