# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# Django
from django import forms

# Local
from .models import Post



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', )