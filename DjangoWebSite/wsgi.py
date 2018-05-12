"""
WSGI config for DjangoWebSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from apscheduler.scheduler import Scheduler
from Blog.views import save_blog_from_api

sched = Scheduler()


@sched.interval_schedule(seconds=3600)
def mytask():
    try:
        save_blog_from_api()
    except Exception as e:
        print("Error: %s" % str(e))
    else:
        print("update blog")


sched.start()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWebSite.settings")

application = get_wsgi_application()
