#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 04/20/18.
"""

from django.db import models

# Create your models here.


# 评论获取
class Comments(models.Model):
    user = models.IntegerField()  # 评论者
    o_type = models.IntegerField()  # 评论的对象类型
    obj = models.IntegerField()  # 评论的对象
    content = models.TextField()  # 评论的内容
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    upvote = models.IntegerField(default=0)  # 点赞量
    deal = models.IntegerField(default=0)  # 是否处理
    status = models.IntegerField(default=0)  # 状态

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(user, o_type, obj, content, date, time):
        comment = Comments()
        comment.user = user
        comment.o_type = o_type
        comment.obj = obj
        comment.content = content
        comment.date = date
        comment.time = time
        comment.save()
        return True, comment.id

    @staticmethod
    def get_comment_by_id(cid):
        try:
            comment = Comments.objects.get(id=cid)
        except Comments.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, comment

    @staticmethod
    def get_all_comments():
        comments = Comments.objects.all().order_by('-id')
        return True, comments

    @staticmethod
    def get_comments_by_user(user):
        comments = Comments.objects.filter(user=user).order_by('-id')
        return True, comments

    @staticmethod
    def get_comments_by_type(o_type):
        comments = Comments.objects.filter(o_type=o_type).order_by('-id')
        return True, comments

    @staticmethod
    def get_comments_by_obj(obj):
        comments = Comments.objects.filter(obj=obj).order_by('-id')
        return True, comments

    @staticmethod
    def get_comments_by_type_obj_status(typ, obj, status):
        # type: (object, object, object) -> object
        comment = Comments.objects.filter(o_type=typ, obj=obj, status=status).order_by('-id')
        return True, comment

    @staticmethod
    def update(cid, user=None, o_type=None, obj=None, content=None, date=None, time=None, upvote=None, deal=None,
               status=None):
        sta, comment = Comments.get_comment_by_id(cid)
        if not sta:
            return sta, comment
        if user is not None:
            comment.user = user
        if o_type is not None:
            comment.o_type = o_type
        if obj is not None:
            comment.obj = obj
        if content is not None:
            comment.content = content
        if date is not None:
            comment.date = date
        if time is not None:
            comment.time = time
        if upvote is not None:
            comment.upvote = upvote
        if deal is not None:
            comment.deal = deal
        if status is not None:
            comment.status = status
        comment.save()
        return True, "update success!"

    @staticmethod
    def delete_comment_by_id(cid):
        sta, comment = Comments.get_comment_by_id(cid=cid)
        if not sta:
            return False, comment
        comment.delete()
        return True, "delete success"
