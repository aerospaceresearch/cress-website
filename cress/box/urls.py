# coding=utf-8
from rest_framework import routers
from django.conf.urls import include, url

from .views import PhotoViewSet, SensorViewSet, BoxActionViewSet, BoxViewSet, CycleViewSet, PlotViewSet
from ax.views import AXTextCreateViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('action', BoxActionViewSet, basename="action")
router_v1.register('box', BoxViewSet, basename="box")
router_v1.register('cycle', CycleViewSet, basename="cycle")
router_v1.register('photo', PhotoViewSet)
router_v1.register('plot', PlotViewSet)
router_v1.register('sensor', SensorViewSet)
router_v1.register('ax-text', AXTextCreateViewSet, basename="ax")


urlpatterns = [
    url(r'^v1/', include(router_v1.urls)),
]
