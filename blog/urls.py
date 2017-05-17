
from django.conf.urls import url, include
from django.contrib import admin


from .apiurls import urlpatterns as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^v1/', include(api_urls))
]
