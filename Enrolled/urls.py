#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import url
from Enrolled import views

urlpatterns = [
    url(r'^$', views.RequestDispatcherView.as_view()),
]
