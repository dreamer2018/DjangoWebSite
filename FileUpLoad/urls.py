#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/5/2.
"""

from django.conf.urls import url

from FileUpLoad import views

urlpatterns = [
    url(r'^$', views.RequestDispatcherView.as_view()),
]
