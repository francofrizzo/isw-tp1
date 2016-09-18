from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('wifindbar.apps.wifindbar.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
