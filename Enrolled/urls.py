#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_enrolled),
                       url(r'^add/$', views.add_enrolled),
                       url(r'^alter/$', views.alter_enrolled),
                       url(r'^delete/$', views.delete_enrolled),
                       url(r'^status/$', views.alter_enrolled_status),
                       )
