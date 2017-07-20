# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3. Party
import six
from google.cloud import translate

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _



class CustomQuerySetManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            # don't delegate internal methods to the queryset
            if attr.startswith('__') and attr.endswith('__'):
                raise
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return self.model.QuerySet(self.model, using=self._db)

class TimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Zamanı"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme Zamanı"))

    class Meta:
        abstract = True


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))

    return result['translatedText']