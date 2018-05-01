# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# Django
from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Local
from apps.utils import TimeStampModel, CustomQuerySetManager



class Post(TimeStampModel):
    """
     Tr => Bu model mesajı ve yazarını bilgisini tutar.
           Ters ilişkide birincil anahtarı olan modeller [MLPost => mlpost_set , Statistics => statistics]
     En => This model keeps message and author information.
           Models with a reverse relational primary key [MLPost, Statistics]
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Yazar"),
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return "{author}-{post}".format(author=self.author, post=self.pk)

    class Meta:
        verbose_name = _("Mesaj")
        verbose_name_plural = _("Mesajlar")



class MultiLanguagePost(models.Model):
    """
     Tr => Bu model mesajları dil tercihine göre tutar.
     En => This model keeps messages according to language preference
    """
    language = models.CharField(
        verbose_name=_("Dil"),
        choices=settings.LANGUAGES,
        max_length=2
    )

    post = models.ForeignKey(
        Post,
        related_name='data',
        verbose_name=_("Mesaj"),
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name=_("Başlık"),
        max_length=155
    )

    content = models.TextField(
        verbose_name=_("Metin"),
        blank=True,
        null=True
    )

    def __str__(self):
        return "{title}".format(title=self.title)

    class Meta:
        verbose_name = _("Mesaj İçeriği")
        verbose_name_plural = _("Mesaj İçerikleri")
        unique_together = ('language', 'post')


# def _create_data_for_other_languages(sender, instance, created, **kwargs):
#     pass
# models.signals.post_save.connect(_create_data_for_other_languages, sender=MultiLanguagePost)

class StatisticsQuerySet(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model, using=self._db)


class Statistics(models.Model):
    """
     Tr => Bu model mesajın istatistiklerini tutar.
     En => This model keeps statistics of the message.
    """

    objects = CustomQuerySetManager()

    DISPLAYED = 'displayed'
    LIKED = 'liked'
    SHARED = 'shared'

    CATEGORIES = (
        ('displayed', _("Görüntülenme")),
        ('liked', _("Beğeni")),
        ('shared', _("Paylaşılma Sayısı"))
    )

    category = models.CharField(
        verbose_name=_("Tür"),
        default='displayed',
        choices=CATEGORIES,
        max_length=8
    )

    post = models.ForeignKey(
        Post,
        related_name='statistics',
        verbose_name=_("Mesaj"),
        on_delete=models.CASCADE,
    )

    ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("IP Adresi")
    )

    created_at = models.DateField(
        auto_now_add=True,
        blank=True,
        verbose_name=_("Oluşturulma Tarihi"),
        help_text=_("Bu sütun kendiliğinden oluşacağı için formda düzenleme dışı kalmalıdır.")
    )

    class QuerySet(QuerySet):
        def get_displayed_by_post(self, post):
            return self.filter(category=Statistics.DISPLAYED, post=post)

        def get_liked_by_post(self, post):
            return self.filter(category=Statistics.LIKED, post=post)

        def get_shared_by_post(self, post):
            return self.filter(category=Statistics.SHARED, post=post)

        def get_by_ip(self, ip):
            return self.filter(ip=ip)

    def __str__(self):
        return "{post}-{category}".format(post=self.post, category=self.category)

    class Meta:
        verbose_name = _("İstatistik")
        verbose_name_plural = _("İstatistikler")

