#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 报名记录
class Enrolled(models.Model):
    obj = models.IntegerField()  # 报名对象
    uid = models.IntegerField()  # 报名者id
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(obj, uid, date, time, status=None):
        enrolled = Enrolled()
        enrolled.obj = obj
        enrolled.uid = uid
        enrolled.date = date
        enrolled.time = time
        if status is not None:
            enrolled.status = status
        enrolled.save()
        return True, enrolled.id

    @staticmethod
    def get_enrolled_by_id(eid):
        try:
            enrolled = Enrolled.objects.get(id=eid)
        except Enrolled.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, enrolled

    @staticmethod
    def get_all_enrolled():
        enrolled = Enrolled.objects.all().order_by('-id')
        return True, enrolled

    @staticmethod
    def get_enrolled_by_obj(obj):
        enrolleds = Enrolled.objects.filter(obj=obj).order_by('-id')
        return True, enrolleds

    @staticmethod
    def get_enrolled_by_status(status):
        enrolled = Enrolled.objects.filter(status=status).order_by('-id')
        return True, enrolled

    @staticmethod
    def update(eid=None, obj=None, uid=None, date=None, time=None, status=None):
        sta, enrolled = Enrolled.get_enrolled_by_id(eid)
        if not sta:
            return sta, enrolled
        if obj is not None:
            enrolled.obj = obj
        if uid is not None:
            enrolled.uid = uid
        if date is not None:
            enrolled.date = date
        if time is not None:
            enrolled.time = time
        if status is not None:
            enrolled.status = status
        enrolled.save()
        return True, "update success!"

    @staticmethod
    def delete_enrolled_by_id(eid):
        sta, enrolled = Enrolled.get_enrolled_by_id(eid=eid)
        if not sta:
            return False, enrolled
        enrolled.delete()
        return True, "delete success"
