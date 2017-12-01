#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 11/2/17.
"""
from django.conf.urls import include, url
import views
import OAuth_Django_SDK

mian_url = [
    url(r'^test/$', views.test),  # /test/
    url(r'^login/$', OAuth_Django_SDK.oauth_login),  # /login/
    url(r'^user/$', OAuth_Django_SDK.get_user_info),  # /user/
    url(r'^news/$', views.get_news),  # /news/
    url(r'^news/add/$', views.add_news),  # /news/add/
    url(r'^news/alter/$', views.alter_news),  # /news/alter/
    url(r'^news/status/$', views.alter_news_status),  # /news/status/
    url(r'^news/delete/$', views.delete_news),  # /news/delete/
    url(r'^events/$', views.get_events),  # /events/
    url(r'^events/add/$', views.add_events),  # /events/add/
    url(r'^events/alter/$', views.alter_events),  # /events/alter/
    url(r'^events/delete/$', views.delete_events),  # /events/delete/
    url(r'^events/status/$', views.alter_events_status),  # /events/status/
    url(r'^projects/$', views.get_projects),
    url(r'^projects/add/', views.add_projects),
    url(r'^projects/alter/', views.alter_projects),
    url(r'^projects/status/', views.alter_projects),
]
