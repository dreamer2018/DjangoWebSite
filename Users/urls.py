#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import patterns, url
import views
import OAuth_Django_SDK

urlpatterns = patterns('',
                       url(r'^anonymous/$', views.get_anonymous),
                       url(r'^anonymous/add/$', views.add_anonymous),
                       url(r'^anonymous/delete/$', views.delete_anonymous),
                       url(r'^devuser/$', views.get_devuser),
                       url(r'^devuser/add/$', views.add_devuser),
                       url(r'^devuser/delete/$', views.delete_devuser),
                       url(r'^devgroup/$', views.get_devgroup),
                       url(r'^devgroup/add/$', views.add_devgroup),
                       url(r'^devgroup/delete/$', views.delete_devgroup),
                       url(r'^devgroup/alter/$', views.alter_devgroup),
                       url(r'^user/me/$', views.get_current_user_info),
                       url(r'^user/$', views.get_all_user_info),
                       url(r'^user/id/$', views.get_user_by_id),
                       url(r'^login/$', OAuth_Django_SDK.oauth_login),  # /login/
                       )
