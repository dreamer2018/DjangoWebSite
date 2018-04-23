#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_news),  # /news/
                       url(r'^add/$', views.add_news),  # /news/add/
                       url(r'^alter/$', views.alter_news),  # /news/alter/
                       url(r'^status/$', views.alter_news_status),  # /news/status/
                       url(r'^delete/$', views.delete_news),  # /news/delete/
                       )
