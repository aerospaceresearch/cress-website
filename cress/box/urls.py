# coding=utf-8
from rest_framework import routers
from django.conf.urls import include, url

from .views import PhotoViewSet, SensorViewSet, BoxActionViewSet, BoxViewSet, CycleViewSet, PlotViewSet
from ax.views import AXTextCreateViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('action', BoxActionViewSet, base_name="action")
router_v1.register('box', BoxViewSet, base_name="box")
router_v1.register('cycle', CycleViewSet, base_name="cycle")
router_v1.register('photo', PhotoViewSet)
router_v1.register('plot', PlotViewSet)
router_v1.register('sensor', SensorViewSet)
router_v1.register('ax-text', AXTextCreateViewSet, base_name="ax")


urlpatterns = [
    url(r'^v1/', include(router_v1.urls)),
]
