#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views
import OAuth_Django_SDK

urlpatterns = patterns('',
                       url(r'^apis/anonymous/$', views.get_anonymous),
                       url(r'^apis/anonymous/add/$', views.add_anonymous),
                       url(r'^apis/anonymous/delete/$', views.delete_anonymous),
                       url(r'^apis/devuser/$', views.get_devuser),
                       url(r'^apis/devuser/add/$', views.add_devuser),
                       url(r'^apis/devuser/delete/$', views.delete_devuser),
                       url(r'^apis/user/me/$', views.get_current_user_info),
                       url(r'^apis/user/$', views.get_all_user_info),
                       url(r'^apis/user/id/$', views.get_user_by_id),
                       url(r'^apis/login/$', OAuth_Django_SDK.oauth_login),  # /login/
                       )
