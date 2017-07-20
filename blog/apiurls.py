# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3. Party
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

# Django
from django.conf.urls import url, include

# Local
from apps.stream import urls as stream_urls


urlpatterns = [
    url(r'^api-token-auth/$', obtain_jwt_token, name="get_token"),
    url(r'^api-token-verify/$', verify_jwt_token),
    url(r'^api-token-refresh/$', refresh_jwt_token),

    url(r'stream/', include(stream_urls, namespace='stream'))
]