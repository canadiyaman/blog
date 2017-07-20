# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Django
from django.conf.urls import url, include

# Local
from .views import PostView

urlpatterns = [
    url(r'^post/(?P<pk>[0-9]+)/$', PostView.as_view(), name="get_post"),
    url(r'^posts/$', PostView.as_view(), name="post_list"),
    url(r'^post/create/$', PostView.as_view(), name="post_create"),
    url(r'^post/remove/(?P<pk>[0-9]+)', PostView.as_view(), name="post_remove"),
    url(r'^post/update/(?P<pk>[0-9]+)', PostView.as_view(), name="post_update")
]