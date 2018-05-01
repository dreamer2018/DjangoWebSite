"""WebSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from Users import views
urlpatterns = patterns('',
                       url(r'^', include("Users.urls", namespace="user")),
                       url(r'^apis/admin/', include(admin.site.urls)),
                       url(r'^apis/blog/', include('Blog.urls', namespace='blog')),
                       url(r'^apis/comments/', include('Comments.urls', namespace='comments')),
                       url(r'^apis/enrolled/', include('Enrolled.urls', namespace='enrolled')),
                       url(r'^apis/events/', include('Events.urls', namespace='events')),
                       url(r'^apis/feedback/', include('Feedback.urls', namespace='feedback')),
                       url(r'^apis/news/', include('News.urls', namespace='news')),
                       url(r'^apis/pictures/', include('Pictures.urls', namespace='pictures')),
                       url(r'^apis/projects/', include('Projects.urls', namespace='projects')),
                       )

handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.server_error
