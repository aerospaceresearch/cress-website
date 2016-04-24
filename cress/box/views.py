from rest_framework import (
    mixins, viewsets, parsers, permissions,
)

from .models import Photo, Sensor, Box
from .serializers import PhotoSerializer, SensorSerializer, BoxActionSerializer


class PhotoUploadViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)


class SensorUploadViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sensor.objects.none()
    serializer_class = SensorSerializer


class BoxActionViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
#    permission_classes = (permissions.IsAuthenticated,)
    permission_classes = ()
    queryset = Box.objects.all()
    serializer_class = BoxActionSerializer
