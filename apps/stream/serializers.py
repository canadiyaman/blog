# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# 3. Party
from rest_framework import serializers

# Local
from .models import (MultiLanguagePost, Statistics, Post)


class MultiLanguagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiLanguagePost
        fields = ('language', 'title', 'content')

class StatisticsCountSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField('get_like_count')
    display = serializers.SerializerMethodField('get_displayed_count')
    share = serializers.SerializerMethodField('get_shared_count')

    def get_like_count(self, obj):
        return obj.filter(category=Statistics.LIKED).count()

    def get_displayed_count(self, obj):
        return obj.filter(category=Statistics.DISPLAYED).count()

    def get_shared_count(self, obj):
        return obj.filter(category=Statistics.SHARED).count()


    class Meta:
        model = Statistics
        fields = ('like', 'display', 'share')


class PostSerializer(serializers.ModelSerializer):
    content = MultiLanguagePostSerializer(source='data', many=True)
    statistic = StatisticsCountSerializer(source='statistics')

    class Meta:
        model = Post
        fields = ('author', 'content', 'statistic')