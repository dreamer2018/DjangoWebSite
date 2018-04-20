#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 匿名用户
class Anonymous(models.Model):
    nickname = models.CharField(max_length=20)  # 昵称
    email = models.CharField(max_length=255)  # 邮件

    def __unicode__(self):
        return self.nickname

    @staticmethod
    def insert(nickname, email):
        anonymous = Anonymous()
        anonymous.nickname = nickname
        anonymous.email = email
        anonymous.save()
        return True, anonymous.id

    @staticmethod
    def get_anonymous_by_id(uid):
        try:
            anonymous = Anonymous.objects.get(id=uid)
        except Anonymous.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, anonymous

    @staticmethod
    def get_all_anonymous():
        anonymous = Anonymous.objects.all()
        return True, anonymous

    @staticmethod
    def get_anonymous_by_email(email):
        anonymous = Anonymous.objects.filter(email__contains=email)
        return True, anonymous

    @staticmethod
    def update(uid, nickname=None, email=None):
        status, anonymous = Anonymous.get_anonymous_by_id(uid)
        if not status:
            return status, anonymous
        if nickname is not None:
            anonymous.nickname = nickname
        if email is not None:
            anonymous.email = email
        anonymous.save()
        return True, "update success!"

    @staticmethod
    def delete_anonymous_by_id(uid):
        status, anonymous = Anonymous.get_anonymous_by_id(uid)
        if not status:
            return False, anonymous
        anonymous.delete()
        return True, "delete success"


# 开发者用户
class Devuser(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(uid, pid):
        devuser = Devuser()
        devuser.uid = uid
        devuser.pid = pid
        devuser.save()
        return True, devuser.id

    @staticmethod
    def get_devuser_by_id(uid):
        try:
            devuser = Devuser.objects.get(id=uid)
        except Devuser.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, devuser

    @staticmethod
    def get_devuser_by_pid(pid):
        devuser = Devuser.objects.filter(pid=pid)
        return True, devuser

    @staticmethod
    def get_all_devuser():
        devuser = Devuser.objects.all()
        return True, devuser

    @staticmethod
    def delete_devuser_by_id(uid):
        sta, devuser = Devuser.get_devuser_by_id(uid=uid)
        if not sta:
            return False, devuser
        devuser.delete()
        return True, "delete success"
