#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_comments),
                       url(r'^add/$', views.add_comments),
                       url(r'^delete/$', views.delete_comments),
                       url(r'^alter/$', views.alter_comments),
                       url(r'^deal/$', views.alter_comments_deal),
                       url(r'^status/$', views.alter_comments_status),
                       )


