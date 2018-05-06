#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_evets),  # /events/
                       url(r'^add/$', views.add_events),  # /events/add/
                       url(r'^alter/$', views.alter_events),  # /events/alter/
                       url(r'^delete/$', views.delete_events),  # /events/delete/
                       url(r'^status/$', views.alter_events_status),  # /events/status/
                       )
