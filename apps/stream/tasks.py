# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import json

from celery.decorators import task

from django.conf import settings

from apps.utils import translate_text


@task(name="apps.stream.create_data_to_post_for_all_languages")
def create_data_to_post_for_all_languages(data, default='tr'):
    from .models import (MultiLanguagePost, Post)


    post = Post.objects.get(pk=data["post"])

    languages = dict(settings.LANGUAGES)
    for language in languages:
        args = {
            "post": post,
            "language": language,
            "title": data["title"],
            "content": data["content"]
        }

        if not language == default:
            args["title"] = translate_text(language, args["title"]),
            args["content"] =translate_text(language, args["content"])


        MultiLanguagePost.objects.create(**args)