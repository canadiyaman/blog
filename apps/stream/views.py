# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


# 3. Party
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Django
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

# Local
from .models import (Post,)
from .serializers import (PostSerializer,)
from .forms import PostForm
from .tasks import (create_data_to_post_for_all_languages,)



class PostView(APIView):
    """
        Allows[GET, LIST, POST, PUT, DELETE]
    """

    permission_classes(IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, pk):
        try:
            post = PostSerializer(Post.objects.get(pk=pk))
            return JsonResponse(post.data, status=200, safe=False)

        except Post.DoesNotExist:
            message = _("Mesaj Bulunamadı")
            return JsonResponse(message, status=404)

    def list(self, request):
        return JsonResponse(PostSerializer(Post.objects.all()).data, status=200, safe=False)


    def post(self, request):
        form = PostForm(request.POST)

        if form.is_valid():
            result = form.save()

            data = {
                "post": result.id,
                "title": request.POST.get('title'),
                "content": request.POST.get("content")
            }
            create_data_to_post_for_all_languages.apply_async(kwargs={"data": data, "default": request.POST.get('language')}, countdown=1)

            message = str(_("Mesaj başarıyla kaydedildi"))
            return JsonResponse({"message": message}, status=201)

        message = "<p>%s</p> : %s" % (str(_("Hatalar")), form.errors)
        return JsonResponse({"message": message}, status=200)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)

            """
                Update staff
            """

            post = PostSerializer(post)
            return JsonResponse(post.data, status=200, safe=False)

        except Post.DoesNotExist:
            message = _("Mesaj Bulunamadı")
            return JsonResponse(message, status=404)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            message = _("Mesaj Silindi")
            status = 200

        except Post.DoesNotExist:
            message = _("Mesaj Bulunamadı")
            status = 404

        return JsonResponse(message, status=status, safe=False)