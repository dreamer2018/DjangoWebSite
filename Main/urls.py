#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""
from django.conf.urls import include, url
import views

mian_url = [
    # /test/
    url(r'^test/$', views.test),
    # /news/
    url(r'^news/$', views.get_news)
]