from rest_framework import (
    mixins, viewsets, parsers, permissions,
)

from .models import Photo
from .serializers import PhotoSerializer


class PhotoUploadViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)
