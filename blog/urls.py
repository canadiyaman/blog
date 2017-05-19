# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# Django
from django.conf.urls import url, include
from django.contrib import admin

# Local
from .apiurls import urlpatterns as api_urls
from apps.user.views import TimelineView

urlpatterns = [

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url('^v1/', include(api_urls)),
    url('^(?P<slug>[\w-]+)/$', TimelineView.as_view(), name="timeline"),
]
