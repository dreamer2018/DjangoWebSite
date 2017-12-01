#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""
from django.db import models


# Create your models here.

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
    def get_anonymous_by_id(id):
        try:
            anonymous = Anonymous.objects.get(id=id)
        except Anonymous.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, anonymous

    @staticmethod
    def update(id, nickname=None, email=None):
        status, anonymous = Anonymous.get_anonymous_by_id(id)
        if not status:
            return status, anonymous
        if nickname is not None:
            anonymous.nickname = nickname
        if email is not None:
            anonymous.email = email
        anonymous.save()
        return True, "update success!"

    @staticmethod
    def delete_anonymous_by_id(id):
        status, anonymous = Anonymous.get_anonymous_by_id(id)
        if not status:
            return False, anonymous
        anonymous.delete()
        return True, "delete success"


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
    def get_events_by_id(id):
        try:
            event = Events.objects.get(id=id)
        except Events.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, event

    @staticmethod
    def get_events_by_title(title):
        events = Events.objects.filter(title=title)
        return True, events

    @staticmethod
    def get_events_by_status(status):
        events = Events.objects.filter(status=status)
        return True, events

    @staticmethod
    def update(id, title=None, content=None, origin=None, date=None, time=None, address=None, labels=None, reader=None,
               upvote=None, enroll=None, poster=None, status=None):
        sta, event = Events.get_events_by_id(id=id)
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
    def delete_events_by_id(id):
        status, event = Events.get_events_by_id(id)
        if not status:
            return False, event
        event.delete()
        return True, "delete success"


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
    def get_feedback_by_id(id):
        try:
            feedback = Feedback.objects.get(id=id)
        except Feedback.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, feedback

    @staticmethod
    def get_feedback_by_title(title):
        feedback = Feedback.objects.filter(title=title)
        return feedback

    @staticmethod
    def get_feedback_by_status(status):
        feedback = Feedback.objects.filter(status=status)
        return feedback

    @staticmethod
    def update(id, email=None, content=None, date=None, time=None, status=None):
        sta, feedback = Feedback.get_feedback_by_id(id=id)
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
    def delete_feedback_by_id(id):
        status, feedback = Feedback.objects.get(id=id)
        if not status:
            return False, feedback
        feedback.delete()
        return True, "delete success"


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
    def get_news_by_id(id):
        try:
            new = News.objects.get(id=id)
        except News.DoesNotExist:
            return False, "Not Found!"
        else:
            return True, new

    @staticmethod
    def get_news_by_title(title):
        news = News.objects.filter(title=title)
        return True, news

    @staticmethod
    def get_news_by_status(status):
        news = News.objects.filter(status=status)
        return True, news

    @staticmethod
    def update(id, title=None, content=None, origin=None, date=None, time=None, labels=None, reader=None,
               upvote=None, poster=None, status=None):
        sta, new = News.get_news_by_id(id=id)
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
    def delete_news_by_id(id):
        status, new = News.get_news_by_id(id=id)
        if not status:
            return False, new
        new.delete()
        return True, "delete success"


class Pictures(models.Model):
    content = models.CharField(max_length=255)  # 照片简介
    link = models.CharField(max_length=255)  # 照片链接
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    upvote = models.IntegerField()  # 点赞量
    status = models.IntegerField(default=0)  # 照片状态

    def __unicode__(self):
        return self.id

    @staticmethod
    def insert(content, link, date, time, upvote, status=None):
        picture = Pictures()
        picture.content = content
        picture.link = link
        picture.date = date
        picture.time = time
        picture.upvote = upvote
        if status is not None:
            picture.status = status
        picture.save()
        return True, picture.id

    @staticmethod
    def get_picture_by_id(id):
        try:
            picture = Pictures.objects.get(id=id)
        except Pictures.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, picture

    @staticmethod
    def get_pictures_by_title(title):
        pictures = Pictures.objects.filter(title=title)
        return pictures

    @staticmethod
    def get_pictures_by_status(status):
        pictures = Pictures.objects.filter(status=status)
        return pictures

    @staticmethod
    def update(id, content=None, link=None, date=None, time=None, upvote=None, status=None):
        sta, picture = Pictures.get_picture_by_id(id=id)
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
        return True, "update success!"

    @staticmethod
    def delete_picture_by_id(id):
        sta, picture = Pictures.objects.get(id=id)
        if not sta:
            return False, picture
        picture.delete()
        return True, "delete success"


class Projects(models.Model):
    title = models.CharField(max_length=50)  # 项目标题
    content = models.TextField()  # 项目内容描述
    origin = models.TextField()  # 项目源内容
    poster = models.CharField(max_length=255)  # 项目标志
    link = models.CharField(max_length=255)  # 项目链接
    date = models.DateField()  # 日期
    time = models.TimeField()  # 时间
    reader = models.IntegerField(default=0)  # 阅读量
    upvote = models.IntegerField(default=0)  # 点赞量
    status = models.IntegerField(default=0)  # 项目状态

    def __unicode__(self):
        return self.title

    @staticmethod
    def insert(gid, title, content, origin, poster, link, date, time):
        project = Pictures()
        project.gid = gid
        project.title = title
        project.content = content
        project.origin = origin
        project.poster = poster
        project.link = link
        project.date = date
        project.time = time
        project.save()
        return True, project.id

    @staticmethod
    def get_all_projects():
        projects = Projects.objects.all()
        return True, projects

    @staticmethod
    def get_project_by_id(id):
        try:
            project = Projects.objects.get(id=id)
        except Projects.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, project

    @staticmethod
    def get_projects_by_title(title):
        projects = Projects.objects.filter(title=title)
        return projects

    @staticmethod
    def get_projects_by_status(status):
        project = Projects.objects.filter(status=status)
        return True, project

    @staticmethod
    def update(id, title=None, content=None, origin=None, poster=None, link=None, date=None, time=None, reader=None,
               upvote=None,
               status=None):
        sta, project = Projects.get_project_by_id(id)
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
        return True, "update success!"

    @staticmethod
    def delete_project_by_id(id):
        sta, project = Projects.objects.get(id=id)
        if not sta:
            return False, project
        project.delete()
        return True, "delete success"


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
    def insert(user, o_type, obj, content, date, time, upvote=None, deal=None, status=None):
        comment = Comments()
        comment.user = user
        comment.o_type = o_type
        comment.obj = obj
        comment.content = content
        comment.date = date
        comment.time = time
        comment.upvote = upvote
        comment.deal = deal
        comment.status = status
        comment.save()
        return True, comment.id

    @staticmethod
    def get_comment_by_id(id):
        try:
            comment = Comments.objects.get(id=id)
        except Comments.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, comment

    @staticmethod
    def get_comments_by_user(user):
        comments = Comments.objects.filter(user=user)
        return True, comments

    @staticmethod
    def get_comments_by_type(type):
        comments = Comments.objects.filter(type=type)
        return True, comments

    @staticmethod
    def get_comments_by_obj(obj):
        comments = Comments.objects.filter(obj=obj)
        return True, comments

    @staticmethod
    def get_comments_by_status(status):
        comment = Comments.objects.filter(status=status)
        return True, comment

    @staticmethod
    def update(id, user=None, o_type=None, obj=None, content=None, date=None, time=None, upvote=None, deal=None,
               status=None):
        sta, comment = Comments.get_comment_by_id(id)
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
    def delete_comment_by_id(id):
        sta, comment = Comments.objects.get(id=id)
        if not sta:
            return False, comment
        comment.delete()
        return True, "delete success"


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
    def get_enrolled_by_id(id):
        try:
            enrolled = Enrolled.objects.get(id=id)
        except Enrolled.DoesNotExist:
            return False, "Not Found！"
        else:
            return True, enrolled

    @staticmethod
    def get_enrolled_by_obj(obj):
        enrolleds = Enrolled.objects.filter(obj=obj)
        return enrolleds

    @staticmethod
    def get_enrolled_by_status(status):
        enrolled = Enrolled.objects.filter(status=status)
        return enrolled

    @staticmethod
    def update(id, obj, uid, date, time, status=None):
        sta, enrolled = Enrolled.get_enrolled_by_id(id)
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
    def delete_enrolled_by_id(id):
        sta, enrolled = Enrolled.objects.get(id=id)
        if not sta:
            return False, enrolled
        enrolled.delete()
        return True, "delete success"


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
    def get_devuser_by_pid(pid):
        devuser = Devuser.objects.filter(pid=pid)
        return True, devuser
