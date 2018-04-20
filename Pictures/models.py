#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 照片墙
class Pictures(models.Model):
    content = models.CharField(max_length=255)  # 照片简介
    link = models.CharField(max_length=255)  # 照片链接
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    upvote = models.IntegerField(default=0)  # 点赞量
    status = models.IntegerField(default=0)  # 照片状态

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(content, link, date, time, status=None):
        picture = Pictures()
        picture.content = content
        picture.link = link
        picture.date = date
        picture.time = time
        if status is not None:
            picture.status = status
        picture.save()
        return True, picture.id

    @staticmethod
    def get_picture_by_id(pid):
        try:
            picture = Pictures.objects.get(id=pid)
        except Pictures.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, picture

    @staticmethod
    def get_all_pictures():
        pictures = Pictures.objects.all()
        return True, pictures

    @staticmethod
    def get_pictures_by_content(content, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            pictures = Pictures.objects.filter(content__contains=content)
        else:
            pictures = Pictures.objects.filter(content=content)
        return True, pictures

    @staticmethod
    def get_pictures_by_status(status):
        pictures = Pictures.objects.filter(status=status)
        return True, pictures

    @staticmethod
    def update(pid, content=None, link=None, date=None, time=None, upvote=None, status=None):
        sta, picture = Pictures.get_picture_by_id(pid=pid)
        if not sta:
            return status, picture
        if content is not None:
            picture.content = content
        if link is not None:
            picture.link = link
        if date is not None:
            picture.date = date
        if time is not None:
            picture.time = time
        if upvote is not None:
            picture.upvote = upvote
        if status is not None:
            picture.status = status
        picture.save()
        return True, "update success!"

    @staticmethod
    def delete_picture_by_id(pid):
        sta, picture = Pictures.get_picture_by_id(pid=pid)
        if not sta:
            return False, picture
        picture.delete()
        return True, "delete success"
