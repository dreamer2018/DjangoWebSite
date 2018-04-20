#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 活动沙龙
class Events(models.Model):
    title = models.CharField(max_length=50)  # 活动标题
    content = models.TextField()  # 活动内容
    origin = models.TextField()  # 活动源内容
    poster = models.CharField(max_length=255, blank=True)  # 海报
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    address = models.CharField(max_length=40)  # 活动地址
    labels = models.CharField(max_length=30)  # 活动标签
    reader = models.IntegerField(default=0)  # 阅读量
    upvote = models.IntegerField(default=0)  # 点赞量
    enroll = models.IntegerField(default=0)  # 报名人数
    status = models.IntegerField(default=0)  # 状态

    def __unicode__(self):
        return self.title

    @staticmethod
    def insert(title, content, origin, date, time, address, labels, reader=None, upvote=None, enroll=None, poster=None,
               status=None):
        events = Events()
        events.title = title
        events.content = content
        events.origin = origin
        events.date = date
        events.time = time
        events.address = address
        events.labels = labels
        if reader is not None:
            events.reader = reader
        if upvote is not None:
            events.upvote = upvote
        if enroll is not None:
            events.enroll = enroll
        if poster is not None:
            events.poster = poster
        if status is not None:
            events.status = status
        events.save()
        return True, events.id

    @staticmethod
    def get_all_events():
        return True, Events.objects.all()

    @staticmethod
    def get_events_by_id(eid):
        try:
            event = Events.objects.get(id=eid)
        except Events.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, event

    @staticmethod
    def get_events_by_title(title, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            events = Events.objects.filter(title__contains=title)
        else:
            events = Events.objects.filter(title=title)
        return True, events

    @staticmethod
    def get_events_by_status(status):
        events = Events.objects.filter(status=status)
        return True, events

    @staticmethod
    def update(eid, title=None, content=None, origin=None, date=None, time=None, address=None, labels=None, reader=None,
               upvote=None, enroll=None, poster=None, status=None):
        sta, event = Events.get_events_by_id(eid=eid)
        if not sta:
            return sta, event
        if title is not None:
            event.title = title
        if content is not None:
            event.content = content
        if origin is not None:
            event.origin = origin
        if date is not None:
            event.date = date
        if time is not None:
            event.time = time
        if address is not None:
            event.address = address
        if labels is not None:
            event.labels = labels
        if reader is not None:
            event.reader = reader
        if upvote is not None:
            event.upvote = upvote
        if enroll is not None:
            event.enroll = enroll
        if poster is not None:
            event.poster = poster
        if status is not None:
            event.status = status
        event.save()
        return True, "update success!"

    @staticmethod
    def delete_events_by_id(eid):
        status, event = Events.get_events_by_id(eid)
        if not status:
            return False, event
        event.delete()
        return True, "delete success"
