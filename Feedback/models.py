#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 反馈
class Feedback(models.Model):
    email = models.CharField(max_length=30)  # 邮箱
    content = models.TextField()  # 反馈内容
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    status = models.IntegerField(default=0)  # 状态

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(email, content, date, time, status=None):
        feedback = Feedback()
        feedback.email = email
        feedback.content = content
        feedback.date = date
        feedback.time = time
        if status is not None:
            feedback.status = status
        feedback.save()
        return True, feedback.id

    @staticmethod
    def get_feedback_by_id(fid):
        try:
            feedback = Feedback.objects.get(id=fid)
        except Feedback.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, feedback

    @staticmethod
    def get_all_feedback():
        feedback = Feedback.objects.all()
        return True, feedback

    @staticmethod
    def get_feedback_by_content(content, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            feedback = Feedback.objects.filter(content__contains=content)
        else:
            feedback = Feedback.objects.filter(content=content)
        return True, feedback

    @staticmethod
    def get_feedback_by_status(status):
        feedback = Feedback.objects.filter(status=status)
        return True, feedback

    @staticmethod
    def update(fid, email=None, content=None, date=None, time=None, status=None):
        sta, feedback = Feedback.get_feedback_by_id(fid=fid)
        if not sta:
            return sta, feedback
        if email is not None:
            feedback.email = email
        if content is not None:
            feedback.content = content
        if date is not None:
            feedback.date = date
        if time is not None:
            feedback.time = time
        if status is not None:
            feedback.status = status
        feedback.save()
        return True, "update success!"

    @staticmethod
    def delete_feedback_by_id(fid):
        status, feedback = Feedback.get_feedback_by_id(fid=fid)
        if not status:
            return False, feedback
        feedback.delete()
        return True, "delete success"
