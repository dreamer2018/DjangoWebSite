#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_projects),
                       url(r'^add/$', views.add_projects),
                       url(r'^alter/$', views.alter_projects),
                       url(r'^status/$', views.alter_projects_status),
                       url(r'^delete/$', views.delete_projects),
                       )
