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
    url(r'^projects/add/$', views.add_projects),
    url(r'^projects/alter/$', views.alter_projects),
    url(r'^projects/status/$', views.alter_projects_status),
    url(r'^projects/delete/$', views.delete_projects),
    url(r'^pictures/$', views.get_pictures),
    url(r'^pictures/add/$', views.add_pictures),
    url(r'^pictures/alter/$', views.alter_pictures),
    url(r'^pictures/status/$', views.alter_pictures_status),
    url(r'^pictures/delete/$', views.delete_pictures),
    url(r'^feedback/$', views.get_feedback),
    url(r'^feedback/add/$', views.add_feedback),
    url(r'^feedback/status/$', views.alter_feedback_status),
    url(r'^feedback/delete/$', views.delete_feedback),
    url(r'^comments/$', views.get_comments),
    url(r'^comments/add/$', views.add_comments),
    url(r'^comments/delete/$', views.delete_comments),
    url(r'^comments/alter/$', views.alter_comments),
    url(r'^comments/deal/$', views.alter_comments_deal),
    url(r'^comments/status/$', views.alter_comments_status),
]
