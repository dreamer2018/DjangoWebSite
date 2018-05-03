#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 项目展示
class Projects(models.Model):
    title = models.CharField(max_length=50)  # 项目标题
    content = models.TextField()  # 项目内容描述
    origin = models.TextField()  # 项目源内容
    poster = models.CharField(max_length=255, blank=True)  # 项目标志
    link = models.CharField(max_length=255)  # 项目链接
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    author = models.IntegerField()  # 作者
    reader = models.IntegerField(default=0)  # 阅读量
    upvote = models.IntegerField(default=0)  # 点赞量
    status = models.IntegerField(default=0)  # 项目状态

    def __unicode__(self):
        return self.title

    @staticmethod
    def insert(title, content, origin, link, date, time, poster=None):
        project = Projects()
        project.title = title
        project.content = content
        project.origin = origin
        project.link = link
        project.date = date
        project.time = time
        if poster is not None:
            project.poster = poster
        project.save()
        return True, project.id

    @staticmethod
    def get_all_projects():
        projects = Projects.objects.all()
        return True, projects

    @staticmethod
    def get_project_by_id(pid):
        try:
            project = Projects.objects.get(id=pid)
        except Projects.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, project

    @staticmethod
    def get_projects_by_title(title, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            projects = Projects.objects.filter(title__contains=title)
        else:
            projects = Projects.objects.filter(title=title)
        return True, projects

    @staticmethod
    def get_projects_by_status(status):
        project = Projects.objects.filter(status=status)
        return True, project

    @staticmethod
    def update(pid, title=None, content=None, origin=None, poster=None, link=None, date=None, time=None, reader=None,
               upvote=None,
               status=None):
        sta, project = Projects.get_project_by_id(pid)
        if not sta:
            return sta, project
        if title is not None:
            project.title = title
        if content is not None:
            project.content = content
        if origin is not None:
            project.origin = origin
        if poster is not None:
            project.poster = poster
        if link is not None:
            project.link = link
        if date is not None:
            project.date = date
        if time is not None:
            project.time = time
        if reader is not None:
            project.reader = reader
        if upvote is not None:
            project.upvote = upvote
        if status is not None:
            project.status = status
        project.save()
        return True, "update success!"

    @staticmethod
    def delete_project_by_id(pid):
        sta, project = Projects.get_project_by_id(pid=pid)
        if not sta:
            return False, project
        project.delete()
        return True, "delete success"
