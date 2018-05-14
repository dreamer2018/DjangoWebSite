#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/4/23.
"""
from django.conf.urls import url
from Users import views
from Users import OAuth_Django_SDK

urlpatterns = [
    url(r'^anonymous/$', views.RequestDispatcherAnonymousView.as_view()),
    url(r'^devuser/$', views.RequestDispatcherDevuserView.as_view()),
    url(r'^devgroup/$', views.RequestDispatcherDevgroupView.as_view()),
    url(r'^user/me/$', views.get_current_user_info),
    url(r'^user/$', views.get_all_user_info),
    url(r'^user/id/$', views.get_user_by_id),
    url(r'^login/$', OAuth_Django_SDK.oauth_login),  # /login/
    url(r'^islogin/$', views.is_login),  # /login/
]
