# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3. Party
from rest_framework import serializers


# Local
from .models import (User, UserTimeline)


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('full_name')
    avatar = serializers.ReadOnlyField(source='avatar.url')

    def full_name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'name')

class UserTimelineSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cover_image = serializers.ReadOnlyField(source='cover_image.url')

    class Meta:
        model = UserTimeline
        fields = ('id', 'user', 'cover_image', 'cover_color', 'slug')
