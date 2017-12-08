#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from models import Anonymous, Events, News, Projects, Pictures, Feedback, Comments, Enrolled, Devuser
import json
from django.views.decorators.csrf import csrf_exempt
from OAuth_Django_SDK import combine_url, GET_USER_INFO_URL
import urllib


# Create your views here.

def test(request):
    anonymous = Anonymous()
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
            'status': True,
            'message': 'success',
            'all_count': len(news),
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
            'status': True,
            'message': 'success',
            'all_count': len(news),
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
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, news = News.get_news_by_status(status=sta)
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(news),
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
def alter_news_status(request):
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
                    new.status = 1
                    sta, message = News.update(id=nid, status=1)
                else:
                    new.status = 0
                    sta, message = News.update(id=nid, status=0)
                rtu = {
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


# 获取活动信息
def get_events(request):
    """/events/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_events(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_events_by_id(request)
            if 'title' in request.GET.keys():
                return get_events_by_title(request)
            if 'status' in request.GET.keys():
                return get_events_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的新闻
def get_all_events(request):
    """/events"""
    status, events = Events.get_all_events()
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(events),
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


# 通过id获取活动内容
def get_events_by_id(request):
    """/events/{id}"""
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
        status, events = Events.get_events_by_id(id)
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


# 通过title获取活动内容
def get_events_by_title(request):
    """/events/{title}"""
    title = request.GET['title']
    status, events = Events.get_events_by_title(title=title)
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(events),
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


# 通过status获取活动内容
def get_events_by_status(request):
    """/events/{status}"""
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
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, events = Events.get_events_by_status(status=sta)
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(events),
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, id = Events.insert(title=title, content=content, origin=origin, date=date, time=time,
                                        labels=labels, address=address, poster=poster)
            else:
                sta, id = Events.insert(title=title, content=content, origin=origin, date=date, time=time,
                                        address=address, labels=labels)
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            if poster is not None:
                sta, message = Events.update(id=eid, title=title, content=content, origin=origin, date=date,
                                             time=time, labels=labels, address=address, poster=poster)
            else:
                sta, message = Events.update(id=eid, title=title, content=content, origin=origin, date=date,
                                             time=time, address=address, labels=labels)
            rtu = {
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, events = Events.get_events_by_id(id=eid)
            if sta:
                if events.status == 0:
                    events.status = 1
                    sta, message = Events.update(id=eid, status=1)
                else:
                    events.status = 0
                    sta, message = Events.update(id=eid, status=0)
                rtu = {
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
                    'status': sta,
                    'message': events
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


# 删除活动
@csrf_exempt
def delete_events(request):
    """/events/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, events = Events.delete_events_by_id(id=eid)
            if sta:
                rtu = {
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
                    'status': sta,
                    'message': events
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 判断用户是否登录


# 获取项目信息
def get_projects(request):
    """/projects/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_projects(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_projects_by_id(request)
            if 'title' in request.GET.keys():
                return get_projects_by_title(request)
            if 'status' in request.GET.keys():
                return get_projects_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的项目信息
def get_all_projects(request):
    """/projects"""
    status, projects = Projects.get_all_projects()
    if status:
        data = []
        for item in projects:
            dic = {
                'pid': item.pid,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'reader': item.reader,
                'upvote': item.upvote,
                'status': item.status
            }
            data.append(dic)
        rtu = {
            'status': True,
            'message': 'success',
            'all_count': len(projects),
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


# 通过id获取项目内容
def get_projects_by_id(request):
    """/projects/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, projects = Projects.get_project_by_id(id)
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
                'reader': projects.reader,
                'upvote': projects.upvote,
                'status': projects.status
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


# 通过title获取项目内容
def get_projects_by_title(request):
    """/projects/{title}"""
    title = request.GET['title']
    status, projects = Projects.get_projects_by_title(title=title)
    if status:
        data = []
        for item in projects:
            dic = {
                'pid': item.pid,
                'title': item.title,
                'content': item.content,
                'origin': item.origin,
                'poster': item.poster,
                'link': item.link,
                'date': item.date.strftime('%Y-%m-%d'),
                'time': item.time.strftime('%H:%M:%S'),
                'reader': item.reader,
                'upvote': item.upvote,
                'status': item.status
            }
            data.append(dic)
        rtu = {
            'status': True,
            'message': 'success',
            'all_count': len(projects),
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


# 通过status获取项目内容
def get_projects_by_status(request):
    """/projects/{status}"""
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
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, projects = Projects.get_projects_by_status(status=sta)
        if status:
            data = []
            for item in projects:
                dic = {
                    'pid': item.pid,
                    'title': item.title,
                    'content': item.content,
                    'origin': item.origin,
                    'poster': item.poster,
                    'link': item.link,
                    'date': item.date.strftime('%Y-%m-%d'),
                    'time': item.time.strftime('%H:%M:%S'),
                    'reader': item.reader,
                    'upvote': item.upvote,
                    'status': item.status
                }
                data.append(dic)
            rtu = {
                'status': True,
                'message': 'success',
                'all_count': len(projects),
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 增加新的项目
@csrf_exempt
def add_projects(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            origin = request.POST['origin']
            link = request.POST['link']
            date = request.POST['date']
            time = request.POST['time']
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
                sta, id = Projects.insert(title=title, content=content, origin=origin, link=link, date=date,
                                          time=time, poster=poster)
            else:
                sta, id = Projects.insert(title=title, content=content, origin=origin, link=link, date=date,
                                          time=time)
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


# 更改项目内容
@csrf_exempt
def alter_projects(request):
    """/projects/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
            title = request.POST['title']
            content = request.POST['content']
            origin = request.POST['origin']
            link = request.POST['link']
            date = request.POST['date']
            time = request.POST['time']
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
                sta, message = Projects.update(id=pid, title=title, content=content, origin=origin, link=link,
                                               date=date, time=time, poster=poster)
            else:
                sta, message = Projects.update(id=pid, title=title, content=content, origin=origin, link=link,
                                               date=date, time=time)
            rtu = {
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
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 更改项目状态
@csrf_exempt
def alter_projects_status(request):
    """/projects/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, projects = Projects.get_project_by_id(id=pid)
            if sta:
                if projects.status == 0:
                    projects.status = 1
                    sta, message = projects.update(id=pid, status=1)
                else:
                    projects.status = 0
                    sta, message = projects.update(id=pid, status=0)
                rtu = {
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
                    'status': sta,
                    'message': projects
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
def delete_projects(request):
    """/projects/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, projects = Projects.delete_project_by_id(id=pid)
            if sta:
                rtu = {
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
                    'status': sta,
                    'message': projects
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 判断用户是否登录


######################################################################################## update 2017.12.01 17:05

# 获取图片信息
def get_pictures(request):
    """/pictures/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_pictures(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_pictures_by_id(request)
            if 'content' in request.GET.keys():
                return get_pictures_by_content(request)
            if 'status' in request.GET.keys():
                return get_pictures_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的图片信息
def get_all_pictures(request):
    """/pictures"""
    status, pictures = Pictures.get_all_pictures()
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(pictures),
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


# 通过id获取图片内容
def get_pictures_by_id(request):
    """/pictures/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, pictures = Pictures.get_picture_by_id(id)
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


# 通过content获取图片内容
def get_pictures_by_content(request):
    """/pictures/{content}"""
    content = request.GET['content']
    status, pictures = Pictures.get_pictures_by_content(content=content)
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(pictures),
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


# 通过status获取图片内容
def get_pictures_by_status(request):
    """/pictures/{status}"""
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
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, pictures = Pictures.get_pictures_by_status(status=sta)
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(pictures),
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Pictures.insert(content=content, link=link, date=date, time=time)
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, message = Pictures.update(id=pid, content=content, link=link, date=date, time=time)
            rtu = {
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, picture = Pictures.get_picture_by_id(id=pid)
            if sta:
                if picture.status == 0:
                    picture.status = 1
                    sta, message = Pictures.update(id=pid, status=1)
                else:
                    picture.status = 0
                    sta, message = Pictures.update(id=pid, status=0)
                rtu = {
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
                    'status': sta,
                    'message': picture
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


# 删除图片
@csrf_exempt
def delete_pictures(request):
    """/pictures/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            pid = int(request.POST['pid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, pictures = Pictures.delete_picture_by_id(id=pid)
            if sta:
                rtu = {
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
                    'status': sta,
                    'message': pictures
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'method error!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)  # 判断用户是否登录


########################################################################################  2017.12.01 19:49 Test Pass

# 获取反馈信息
def get_feedback(request):
    """/feedback/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_feedback(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_feedback_by_id(request)
            if 'content' in request.GET.keys():
                return get_feedback_by_content(request)
            if 'status' in request.GET.keys():
                return get_feedback_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的反馈信息
def get_all_feedback(request):
    """/feedback"""
    status, feedback = Feedback.get_all_feedback()
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(feedback),
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


# 通过id获取反馈内容
def get_feedback_by_id(request):
    """/feedback/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, feedback = Feedback.get_feedback_by_id(id)
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


# 通过content获取反馈内容
def get_feedback_by_content(request):
    """/feedback/{content}"""
    content = request.GET['content']
    status, feedback = Feedback.get_feedback_by_content(content=content)
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(feedback),
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


# 通过status获取反馈内容
def get_feedback_by_status(request):
    """/feedback/{status}"""
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
        # if sta == 0:
        #     if not is_login(request)[0]:
        #         return HttpResponseRedirect('/login/?next=' + request.path)
        status, feedback = Feedback.get_feedback_by_status(status=sta)
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(feedback),
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Feedback.insert(content=content, email=email, date=date, time=time)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'fid': id
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


# 更改反馈状态
@csrf_exempt
def alter_feedback_status(request):
    """/feedback/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            fid = int(request.POST['fid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, feedback = Feedback.get_feedback_by_id(id=fid)
            if sta:
                if feedback.status == 0:
                    feedback.status = 1
                    sta, message = Feedback.update(id=fid, status=1)
                else:
                    feedback.status = 0
                    sta, message = Feedback.update(id=fid, status=0)
                rtu = {
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
                    'status': sta,
                    'message': feedback
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


# 删除反馈
@csrf_exempt
def delete_feedback(request):
    """/feedback/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            fid = int(request.POST['fid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, feedback = Feedback.delete_feedback_by_id(id=fid)
            if sta:
                rtu = {
                    'status': sta,
                    'message': feedback,
                    'data': {
                        'fid': fid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': feedback
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


########################################################################################  2017.12.04 18:11 Test Pass

# 获取评论信息
def get_comments(request):
    """/comments/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_comments(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_comments_by_id(request)
            if 'user' in request.GET.keys():
                return get_comments_by_user(request)
            if 'type' in request.GET.keys():
                return get_comments_by_type(request)
            if 'obj' in request.GET.keys():
                return get_comments_by_obj(request)
            if 'status' in request.GET.keys():
                return get_comments_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的评论信息
def get_all_comments(request):
    """/comments"""
    status, comments = Comments.get_all_comments()
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(comments),
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


# 通过id获取评论内容
def get_comments_by_id(request):
    """/comments/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, comments = Comments.get_comment_by_id(id)
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


# 通过用户ID获取评论内容
def get_comments_by_user(request):
    """/comments/{user}"""
    try:
        str_user = request.GET['user']
        user = int(str_user)
        status, comments = Comments.get_comments_by_user(user=user)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(comments),
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


# 通过o_type获取评论内容
def get_comments_by_type(request):
    """/comments/{type}"""
    try:
        str_type = request.GET['type']
        type = int(str_type)
        status, comments = Comments.get_comments_by_type(type=type)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(comments),
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


# 通过评论对象获取评论内容
def get_comments_by_obj(request):
    """/comments/{type}"""
    try:
        str_obj = request.GET['obj']
        obj = int(str_obj)
        status, comments = Comments.get_comments_by_obj(obj=obj)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(comments),
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


# 通过status获取反馈内容
def get_comments_by_status(request):
    """/comments/{status}"""
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
        status, comments = Comments.get_comments_by_status(status=sta)
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(comments),
                'data': data
            }
            js = json.dumps(rtu)
            return HttpResponse(js)


# 增加新的反馈
@csrf_exempt
def add_comments(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            user = request.POST['user']
            type = request.POST['type']
            obj = request.POST['obj']
            content = request.POST['content']
            date = request.POST['date']
            time = request.POST['time']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Comments.insert(user=user, o_type=type, obj=obj, content=content, date=date, time=time)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'cid': id
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


# 删除评论
@csrf_exempt
def delete_comments(request):
    """/comments/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)

    if request.method == 'POST':
        try:
            cid = int(request.POST['cid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, comments = Comments.delete_comment_by_id(id=cid)
            if sta:
                rtu = {
                    'status': sta,
                    'message': comments,
                    'data': {
                        'fid': cid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': comments
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


# 更该评论内容
@csrf_exempt
def alter_comments(request):
    """/comments/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            cid = int(request.POST['cid'])
            user = request.POST['user']
            type = request.POST['type']
            obj = request.POST['obj']
            content = request.POST['content']
            date = request.POST['date']
            time = request.POST['time']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, message = Comments.update(id=cid, user=user, o_type=type, obj=obj, content=content, date=date,
                                           time=time)
            rtu = {
                'status': sta,
                'message': message,
                'data': {
                    'id': cid
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


# 更改deal状态
@csrf_exempt
def alter_comments_deal(request):
    """/comments/deal/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            cid = int(request.POST['cid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, comments = Comments.get_comment_by_id(id=cid)
            if sta:
                if comments.deal == 0:
                    comments.deal = 1
                    sta, message = Comments.update(id=cid, deal=1)
                else:
                    comments.deal = 0
                    sta, message = comments.update(id=cid, deal=0)
                rtu = {
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
                    'status': sta,
                    'message': comments
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


# 更改评论状态
@csrf_exempt
def alter_comments_status(request):
    """/comments/status/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            cid = int(request.POST['cid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, comments = Comments.get_comment_by_id(id=cid)
            if sta:
                if comments.status == 0:
                    comments.status = 1
                    sta, message = Comments.update(id=cid, status=1)
                else:
                    comments.status = 0
                    sta, message = comments.update(id=cid, status=0)
                rtu = {
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
                    'status': sta,
                    'message': comments
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


########################################################################################  2017.12.04 19:54 Test Pass


# 获取匿名用户信息
def get_anonymous(request):
    """/anonymous/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_anonymous(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_anonymous_by_id(request)
            if 'email' in request.GET.keys():
                return get_anonymous_by_email(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有的匿名用户信息
def get_all_anonymous(request):
    """/anonymous"""
    status, anonymous = Anonymous.get_all_anonymous()
    if status:
        data = []
        for item in anonymous:
            dic = {
                'aid': item.id,
                'email': item.email,
                'nickname': item.nickname
            }
            data.append(dic)
        rtu = {
            'status': True,
            'message': 'success',
            'all_count': len(anonymous),
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


# 通过id获取匿名用户信息
def get_anonymous_by_id(request):
    """/anonymous/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, anonymous = Anonymous.get_anonymous_by_id(id)
        if status:
            data = {
                'aid': anonymous.id,
                'email': anonymous.email,
                'nickname': anonymous.nickname
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


# 通过email获取匿名用户
def get_anonymous_by_email(request):
    """/anonymous/{content}"""
    email = request.GET['email']
    status, anonymous = Anonymous.get_anonymous_by_email(email=email)
    if status:
        data = []
        for item in anonymous:
            dic = {
                'aid': item.id,
                'email': item.email,
                'nickname': item.nickname
            }
            data.append(dic)
        rtu = {
            'status': True,
            'message': 'success',
            'all_count': len(anonymous),
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


# 增加新的匿名用户信息
@csrf_exempt
def add_anonymous(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            email = request.POST['email']
            nickname = request.POST['nickname']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Anonymous.insert(nickname=nickname, email=email)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'nid': id
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


# 更改匿名用户信息
@csrf_exempt
def alter_anonymous(request):
    """/anonymous/alter/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            nid = int(request.POST['nid'])
            email = request.POST['email']
            nickname = request.POST['nickname']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, anonymous = Anonymous.get_anonymous_by_id(id=nid)
            if sta:
                sta, message = Anonymous.update(id=nid, email=email, nickname=nickname)
                rtu = {
                    'status': sta,
                    'message': message,
                    'data': {
                        'status': anonymous.id
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': anonymous
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


# 删除匿名用户信息
@csrf_exempt
def delete_anonymous(request):
    """/anonymous/delete/"""
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
            sta, anonymous = Anonymous.delete_anonymous_by_id(id=nid)
            if sta:
                rtu = {
                    'status': sta,
                    'message': anonymous,
                    'data': {
                        'fid': nid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': anonymous
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


########################################################################################  2017.12.04 20:23 Test Pass


# 获取报名记录
def get_enrolled(request):
    """/enrolled/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_enrolled(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_enrolled_by_id(request)
            if 'obj' in request.GET.keys():
                return get_enrolled_by_obj(request)
            if 'status' in request.GET.keys():
                return get_enrolled_by_status(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有报名信息
def get_all_enrolled(request):
    """/enrolled"""
    status, enrolled = Enrolled.get_all_enrolled()
    if status:
        data = []
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
            'status': True,
            'message': 'success',
            'all_count': len(enrolled),
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


# 通过id获取报名信息
def get_enrolled_by_id(request):
    """/enrolled/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, enrolled = Enrolled.get_enrolled_by_id(id)
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


# 通过obj获取报名信息
def get_enrolled_by_obj(request):
    """/enrolled/{obj}"""
    try:
        str_obj = request.GET['obj']
        obj = int(str_obj)
        status, enrolled = Enrolled.get_enrolled_by_obj(obj=obj)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid arguments!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(enrolled),
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


# 通过status获取报名信息
def get_enrolled_by_status(request):
    """/enrolled/{status}"""
    try:
        str_status = request.GET['status']
        sta = int(str_status)
        status, enrolled = Enrolled.get_enrolled_by_status(status=sta)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
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
                'status': True,
                'message': 'success',
                'all_count': len(enrolled),
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


# 增加新的报名用户信息
@csrf_exempt
def add_enrolled(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            obj = int(request.POST['obj'])
            uid = int(request.POST['uid'])
            date = request.POST['date']
            time = request.POST['time']
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Enrolled.insert(obj=obj, uid=uid, date=date, time=time)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'eid': id
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
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, enrolled = Enrolled.get_enrolled_by_id(id=eid)
            if sta:
                if status is not None:
                    sta, message = Enrolled.update(id=eid, obj=obj, uid=uid, date=date, time=time, status=status)
                else:
                    sta, message = Enrolled.update(id=eid, obj=obj, uid=uid, date=date, time=time)
                rtu = {
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
                    'status': sta,
                    'message': enrolled
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


# 删除报名信息
@csrf_exempt
def delete_enrolled(request):
    """/enrolled/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            eid = int(request.POST['eid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, enrolled = Enrolled.delete_enrolled_by_id(id=eid)
            if sta:
                rtu = {
                    'status': sta,
                    'message': enrolled,
                    'data': {
                        'eid': eid
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': enrolled
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


########################################################################################  2017.12.04 21:08 Test Pass

# 获取开发者信息
def get_devuser(request):
    """/devuser/"""
    if request.method == 'GET':
        if len(request.GET) == 0:
            return get_all_devuser(request)
        elif len(request.GET) > 1 or len(request.GET) < 0:
            pass
        else:
            if 'id' in request.GET.keys():
                return get_devuser_by_id(request)
            if 'pid' in request.GET.keys():
                return get_devuser_by_pid(request)
    rtu = {
        'status': False,
        'message': 'invalid argument',
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


# 获取所有开发者信息
def get_all_devuser(request):
    """/devuser"""
    status, devuser = Devuser.get_all_devuser()
    if status:
        data = []
        for item in devuser:
            dic = {
                'did': item.id,
                'uid': item.uid,
                'pid': item.pid
            }
            data.append(dic)
        rtu = {
            'status': True,
            'message': 'success',
            'all_count': len(devuser),
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


# 通过id获取开发者信息
def get_devuser_by_id(request):
    """/devuser/{id}"""
    try:
        str_id = request.GET['id']
        id = int(str_id)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid argument!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        status, devuser = Devuser.get_devuser_by_id(id=id)
        if status:
            data = {
                'did': devuser.id,
                'uid': devuser.uid,
                'pid': devuser.pid
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


# 通过obj获取开发者信息
def get_devuser_by_pid(request):
    """/devuser/{obj}"""
    try:
        str_pid = request.GET['pid']
        pid = int(str_pid)
        status, devuser = Devuser.get_devuser_by_pid(pid=pid)
    except Exception, e:
        rtu = {
            'status': False,
            'message': 'invalid arguments!'
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    else:
        if status:
            data = []
            for item in devuser:
                dic = {
                    'did': item.id,
                    'uid': item.uid,
                    'pid': item.pid
                }
                data.append(dic)
            rtu = {
                'status': True,
                'message': 'success',
                'all_count': len(devuser),
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


# 增加新的开发者信息
@csrf_exempt
def add_devuser(request):
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            uid = int(request.POST['uid'])
            pid = int(request.POST['pid'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, id = Devuser.insert(uid=uid, pid=pid)
            rtu = {
                'status': sta,
                'message': 'success',
                'data': {
                    'eid': id
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


# 删除开发者
@csrf_exempt
def delete_devuser(request):
    """/devuser/delete/"""
    # if not is_login(request)[0]:
    #     return HttpResponseRedirect('/login/?next=' + request.path)
    if request.method == 'POST':
        try:
            did = int(request.POST['did'])
        except Exception, e:
            rtu = {
                'status': False,
                'message': 'invalid argument',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            sta, devuser = Devuser.delete_devuser_by_id(id=did)
            if sta:
                rtu = {
                    'status': sta,
                    'message': devuser,
                    'data': {
                        'eid': did
                    }
                }
                js = json.dumps(rtu)
                return HttpResponse(js)
            else:
                rtu = {
                    'status': sta,
                    'message': devuser
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
        except IOError, e:
            rtu = {
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'user not login!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 获取所有用户信息
def get_all_user_info(request):
    if 'login' in request.session.keys() and request.session['login']:
        access_token = request.session['access_token']
        url = "https://api.xiyoulinux.org/users?page=1&per_page=1&access_token=%s" % access_token
        params = urllib.unquote(url)
        try:
            response = urllib.urlopen(params)
        except IOError, e:
            rtu = {
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
            'status': False,
            'message': 'user not login!',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)


# 获取所有用户信息
def get_user_by_id(request):
    if 'id' not in request.GET.keys():
        rtu = {
            'status': False,
            'message': 'invalid argument',
        }
        js = json.dumps(rtu)
        return HttpResponse(js)
    try:
        int(request.GET['id'])
    except Exception:
        rtu = {
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
        except IOError, e:
            rtu = {
                'status': False,
                'message': 'login out of time!',
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
        else:
            rtu = {
                'status': True,
                'message': 'success',
                'data': json.loads(response.read())
            }
            js = json.dumps(rtu)
            return HttpResponse(js)
    else:
        rtu = {
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
            response = urllib.urlopen(params)
        except IOError, e:
            request.session['login'] = False
            return False, 'login out of time!'
        else:
            return True, 'login success!'
    else:
        return False, 'not login!'
