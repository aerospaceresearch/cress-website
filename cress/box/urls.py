# coding=utf-8
from rest_framework import routers
from django.conf.urls import include, url

from .views import PhotoUploadViewSet, SensorUploadViewSet, BoxActionViewSet, BoxViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('box', BoxViewSet, base_name="box")
router_v1.register('photo', PhotoUploadViewSet)
router_v1.register('sensor', SensorUploadViewSet)
router_v1.register('action', BoxActionViewSet, base_name="action")


urlpatterns = [
    url(r'^v1/', include(router_v1.urls)),
]
