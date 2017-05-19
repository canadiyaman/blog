# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3. Party
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Django
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

# Local
from .models import UserTimeline
from .serializers import UserTimelineSerializer



class TimelineView(APIView):
    """
    Allows ['GET' - > returned UserTimeline object as json]
    """


    # permission_classes(IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication,)


    def get(self, request, slug):
        try:
            timeline = UserTimelineSerializer(UserTimeline.objects.get(slug=slug))
            return JsonResponse(timeline.data, status=200, safe=False)
        except UserTimeline.DoesNotExist:
            message = str(_("Bulunamadı"))
            return JsonResponse(message, status=404, safe=False)