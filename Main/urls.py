#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""
from django.conf.urls import include, url
import views
import OAuth_Django_SDK

mian_url = [
    # /test/
    url(r'^test/$', views.test),
    # /news/
    url(r'^news/$', views.get_news),
    # /login/
    url(r'^login/$', OAuth_Django_SDK.oauth_login),
    # /user/
    url(r'^user/$', OAuth_Django_SDK.get_user_info),
    # /news/add/
    url(r'^news/add/$', views.add_news),
    # /news/alter/
    url(r'^news/alter/$', views.alter_news),
    # /news/status/
    url(r'^news/status/$', views.alter_status),
    # /news/delete/
    url(r'^news/delete/$', views.delete_news),

]
