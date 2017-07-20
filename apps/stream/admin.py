# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# Django
from django.contrib import admin




# Local
from .models import (MultiLanguagePost, Statistics, Post)



class MultiLanguagePostInline(admin.TabularInline):
    model = MultiLanguagePost
    verbose_name = MultiLanguagePost._meta.verbose_name
    verbose_name_plural = MultiLanguagePost._meta.verbose_name_plural


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    raw_id_fields = ('author',)
    autocomplete_lookup_fields = {
        'fk': ['author', ],
    }

    search_fields = ("data__title", "data__ip")

    inlines = (MultiLanguagePostInline, )

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).select_related().prefetch_related()

@admin.register(Statistics)
class Statistics(admin.ModelAdmin):

    list_display = ('category', 'post')

    list_filter = ('category', 'post')

    search_fields = ('ip',)

    raw_id_fields = ('post',)
    autocomplete_lookup_fields = {
        'fk': ['post', ],
    }

    def get_queryset(self, request):
        return super(Statistics, self).get_queryset(request).select_related().prefetch_related()


