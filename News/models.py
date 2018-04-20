#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 新闻动态
class News(models.Model):
    title = models.CharField(max_length=50)  # 新闻标题
    content = models.TextField()  # 新闻内容
    origin = models.TextField()  # 新闻源内容
    poster = models.CharField(max_length=255, blank=True)  # 新闻图片
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    labels = models.CharField(max_length=30)  # 新闻标签
    reader = models.IntegerField(default=0)  # 阅读量
    upvote = models.IntegerField(default=0)  # 点赞量
    status = models.IntegerField(default=0)  # 新闻状态

    def __unicode__(self):
        return self.title

    @staticmethod
    def insert(title, content, origin, date, time, labels, poster=None, reader=None, upvote=None, status=None):
        new = News()
        new.title = title
        new.content = content
        new.origin = origin
        new.date = date
        new.time = time
        new.labels = labels
        if poster is not None:
            new.poster = poster
        if reader is not None:
            new.reader = reader
        if upvote is not None:
            new.upvote = upvote
        if status is not None:
            new.status = status
        new.save()
        return True, new.id

    @staticmethod
    def get_all_news():
        return True, News.objects.all()

    @staticmethod
    def get_news_by_id(nid):
        try:
            new = News.objects.get(id=nid)
        except News.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, new

    @staticmethod
    def get_news_by_title(title, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            news = News.objects.filter(title__contains=title)
        else:
            news = News.objects.filter(title=title)
        return True, news

    @staticmethod
    def get_news_by_status(status):
        news = News.objects.filter(status=status)
        return True, news

    @staticmethod
    def update(nid, title=None, content=None, origin=None, date=None, time=None, labels=None, reader=None,
               upvote=None, poster=None, status=None):
        sta, new = News.get_news_by_id(nid=nid)
        if not sta:
            return sta, new
        if title is not None:
            new.title = title
        if content is not None:
            new.content = content
        if origin is not None:
            new.origin = origin
        if date is not None:
            new.date = date
        if time is not None:
            new.time = time
        if labels is not None:
            new.labels = labels
        if reader is not None:
            new.reader = reader
        if upvote is not None:
            new.upvote = upvote
        if poster is not None:
            new.poster = poster
        if status is not None:
            new.status = status
        new.save()
        return True, "update success!"

    @staticmethod
    def delete_news_by_id(nid):
        status, new = News.get_news_by_id(nid=nid)
        if not status:
            return False, new
        new.delete()
        return True, "delete success"
