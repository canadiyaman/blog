# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


import uuid
from os.path import splitext


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
# Create your models here.


def _handle_avatar_upload(instance, filename):
    name, extension = splitext(filename)
    new_filename = "{0}{1}".format(uuid.uuid4(), extension)
    return "{0}/{1}".format("avatars", new_filename)

def _handle_cover_image_upload(instance, filename):
    name, extension = splitext(filename)
    new_filename = "{0}{1}".format(uuid.uuid4(), extension)
    return "{0}/{1}".format("coverimages", new_filename)


class User(AbstractUser):

    avatar = models.ImageField(
        verbose_name=_("Profil Resmi"),
        default=settings.DEFAULT_AVATAR_IMAGE,
        upload_to=_handle_avatar_upload,
    )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = _("Kullanıcı")
        verbose_name_plural = _("Kullanıcılar")

class UserTimeline(models.Model):

    user = models.OneToOneField(
        User,
        verbose_name=_("Kullanıcı")
    )

    cover_imnage = models.ImageField(
        verbose_name=_("Duvar Resmi"),
        default=settings.DEFAULT_COVER_IMAGE,
        upload_to=_handle_cover_image_upload
    )
    cover_color = models.CharField(
        verbose_name=_("Duvar Rengi"),
        default="FFFFFF",
        max_length=6
    )

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = _("Zaman Tüneli")
        verbose_name_plural = _("Zaman Tünelleri")