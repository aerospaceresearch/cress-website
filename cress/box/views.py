from rest_framework import (
    mixins, viewsets, parsers, permissions,
)

from .models import Photo, Sensor
from .serializers import PhotoSerializer, SensorSerializer


class PhotoUploadViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)


class SensorUploadViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
#    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sensor.objects.none()
    serializer_class = SensorSerializer
