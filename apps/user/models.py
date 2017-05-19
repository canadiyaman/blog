# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# 3. Party
import uuid
from os.path import splitext

#Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _



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


def _create_user_timeline(sender, instance, created, **kwargs):
    if created:
        UserTimeline.objects.create(user=instance)

signals.post_save.connect(_create_user_timeline, sender=User)


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

    slug = models.CharField(
        default="",
        max_length=255,
        verbose_name=_("Zaman Tüneli Linki")
    )

    def get_absolute_url(self):

        return reverse('timeline', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify("%s-%s" % (self.user.first_name, self.user.last_name))
        super(UserTimeline, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = _("Zaman Tüneli")
        verbose_name_plural = _("Zaman Tünelleri")