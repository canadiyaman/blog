# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local
from .models import (User, UserTimeline)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'is_staff', 'username')
    list_filter = ('username', 'first_name', 'email')

    fieldsets = (
        (_("Hesap Bilgileri"), {  # 1. açılır-kapanır tab başlığı
            'classes': ('grp-collapse grp-open',),  # tab stili
            'fields': ('is_active', 'username', 'password',)  # tab içinde hangi alanlar olacak
        }),
        (_("Kullanıcı Bilgileri"), {
            'classes': ('grp-collapse grp-open',),
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_("Profil"), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('avatar',)
        })
    )


@admin.register(UserTimeline)
class UserTimeline(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user__username',)
