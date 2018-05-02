#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/5/2.
"""


from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.upload),
                       )
