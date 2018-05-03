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


class Devgroup(models.Model):
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)

    @staticmethod
    def insert(name, desc):
        devgroup = Devgroup()
        devgroup.name = name
        devgroup.desc = desc
        devgroup.save()
        return True, devgroup.id

    @staticmethod
    def update(gid, name, desc):
        sta, devgroup = Devgroup.get_devgroup_by_id(gid=gid)
        if not sta:
            return sta, devgroup
        devgroup.name = name
        devgroup.desc = desc
        devgroup.save()
        return True, devgroup.id

    @staticmethod
    def get_devgroup_by_id(gid):
        try:
            devgroup = Devgroup.objects.get(id=gid)
        except Devgroup.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, devgroup

    @staticmethod
    def get_devgroup_by_title(name, sign=0):
        # sign 精确查询与模糊查询选项 0 为模糊查询(默认) 非0 为精确查询
        if sign == 0:
            devgroup = Devgroup.objects.filter(name__contains=name)
        else:
            devgroup = Devgroup.objects.filter(name=name)
        return True, devgroup

    @staticmethod
    def get_all_devgroup():
        devgroup = Devgroup.objects.all()
        return True, devgroup

    @staticmethod
    def delete_devgroup_by_id(gid):
        sta, devgroup = Devgroup.get_devgroup_by_id(gid=gid)
        if not sta:
            return False, devgroup
        devgroup.delete()
        return True, "delete success"


# 开发者用户
class Devuser(models.Model):
    nickname = models.CharField(max_length=20)  # 昵称
    email = models.CharField(max_length=255)  # 邮件
    gid = models.IntegerField()

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(nickname, email, gid):
        devuser = Devuser()
        devuser.nickname = nickname
        devuser.email = email
        devuser.gid = gid
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
    def get_devuser_by_gid(gid):
        devuser = Devuser.objects.filter(gid=gid)
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
