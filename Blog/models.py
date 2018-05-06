#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=50)  # 文章标题
    author = models.CharField(max_length=20)  # 文章作者
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    summary = models.TextField()  # 内容摘要
    url = models.CharField(max_length=256)  # url
    status = models.IntegerField(default=0)  # 状态,0 为未发布， 1 为已发布

    def __unicode__(self):
        return self.title

    @staticmethod
    def insert(title, author, date, time, summary, url, status=None):
        blog = Blog()
        blog.title = title
        blog.author = author
        blog.date = date
        blog.time = time
        blog.summary = summary
        blog.url = url

        if status:
            blog.status = status
        blog.save()

        return True, blog.id

    @staticmethod
    def get_all_blogs():
        return True, Blog.objects.all().order_by('-id')

    @staticmethod
    def get_blog_by_id(bid):
        try:
            blog = Blog.objects.get(id=bid)
        except Blog.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, blog

    @staticmethod
    def get_blog_by_title(title, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            blog = Blog.objects.filter(title__contains=title).order_by('-id')
        else:
            blog = Blog.objects.filter(title=title).order_by('-id')
        return True, blog

    @staticmethod
    def get_blog_by_status(status):
        blog = Blog.objects.filter(status=status).order_by('-id')
        return True, blog

    @staticmethod
    def alter_blog_status(bid, status):
        sta, blog = Blog.get_blog_by_id(bid)
        if not sta:
            return False, blog
        blog.status = status
        blog.save()
        return True, "alter success"

    @staticmethod
    def delete_blog_by_id(bid):
        status, blog = Blog.get_blog_by_id(bid)
        if not status:
            return False, blog
        blog.delete()
        return True, "delete success"
