#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by ZhouPan at 2018/5/2.
"""


from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
import views

urlpatterns = patterns('',
                       url(r'^$', views.upload),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
