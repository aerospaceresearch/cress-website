# coding=utf-8
from rest_framework import routers
from django.conf.urls import include, url

from .views import PhotoUploadViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('photo', PhotoUploadViewSet)


urlpatterns = [
    url(r'^v1/', include(router_v1.urls)),
]
