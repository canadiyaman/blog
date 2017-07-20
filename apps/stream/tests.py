# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3. Party
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

#Django
from django.core.urlresolvers import reverse

# Local
from apps.user.models import User


class PostCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('can', 'can@adiyaman.com', 'canpassword')
        self.token = self.get_token()

        self.data = {
            "title": "Merhaba Blog !",
            "content": """
                        <h3>Heading in h3, som more sample text</h3>
                        <p>Nulla facilisi. Nullam cursus scelerisque erat. Praesent convallis rhoncus dui. In hac habitasse platea dictumst. Nullam pellentesque. Mauris ac orci. Donec dictum. Etiam purus tortor, elementum a, posuere nec, pulvinar id, ipsum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque vel justo. Nullam posuere purus sed arcu.</p>
                        <ul>
                            <li>Nulla facilisi.</li>
                            <li>Pellentesque habitant morbi</li>
                            <li>Quisque vel justo.</li>
                            <li>Nullam posuere purus sed arcu.</li>
                        </ul>
                        """,
            "author": self.superuser.id,
            "language": "tr"
        }

    def test_can_create_post(self):
        response = self.client.post(reverse('v1:stream:post_create'), self.data,  HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_get(self):
        response = self.client.get(reverse('v1:stream:get_post', kwargs={"pk": 1}), HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_post(self):
        pass

    def test_can_remove_post(self):
        response = self.client.get(reverse('v1:stream:post_remove', kwargs={"pk": 1}), {}, HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_token(self):
        return self.client.post(reverse('v1:get_token'), {"username": "can", "password": "canpassword"}).data['token']






# factory = APIRequestFactory()
#
#
# request = factory.post('/v1/stream/posts/', {}, content_type="application/json")
# print(request)



#
# class ReadUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.user = User.objects.create(username="mike")
#
#     def test_can_read_user_list(self):
#         response = self.client.get(reverse('user-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_can_read_user_detail(self):
#         response = self.client.get(reverse('user-detail', args=[self.user.id]))
# self.assertEqual(response.status_code, status.HTTP_200_OK)