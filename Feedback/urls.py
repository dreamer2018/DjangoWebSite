#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_feedback),
                       url(r'^add/$', views.add_feedback),
                       url(r'^status/$', views.alter_feedback_status),
                       url(r'^delete/$', views.delete_feedback),
                       )
