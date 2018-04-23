#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_pictures),
                       url(r'^add/$', views.add_pictures),
                       url(r'^alter/$', views.alter_pictures),
                       url(r'^status/$', views.alter_pictures_status),
                       url(r'^delete/$', views.delete_pictures),
                       )
