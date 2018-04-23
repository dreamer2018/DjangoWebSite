#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_blog),  # /blog/
                       url(r'^add/$', views.add_blog),  # /blog/add
                       url(r'^status/$', views.alter_blog_status),  # /blog/status/
                       url(r'^delete/$', views.delete_blog),  # /blog/delete/
                       )
