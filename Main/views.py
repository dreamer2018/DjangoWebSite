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
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
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
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
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

        # 更改新闻内容


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


# 更改新闻状态
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


# 删除新闻
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
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
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

        # 更改新闻内容


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


# 更改新闻状态
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


# 通过title获取图片内容
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
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
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


# 删除新闻
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


# 通过title获取反馈内容
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
        if sta == 0:
            if not is_login(request)[0]:
                return HttpResponseRedirect('/login/?next=' + request.path)
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


# 判断用户是否登录
def is_login(request):
    if 'login' in request.session.keys() and request.session['login']:
        return True, request.session['user']
    else:
        return False, None
