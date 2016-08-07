from django.utils import timezone
from rest_framework import (
    mixins, viewsets, parsers, permissions, response
)

from .models import Photo, Sensor, Box
from .serializers import PhotoSerializer, SensorSerializer, BoxActionSerializer, BoxSerializer


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


class BoxActionViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Box.objects.all()
    serializer_class = BoxActionSerializer

    def create(self, request, *args, **kwargs):
        from box.models import Cycle
        from box.serializers import ActionSerializer
        pk = request.data.get('box')
        current_cycle = Cycle.objects.filter(active=True).filter(box__id=pk).order_by('-modified').first()
        dt = timezone.now()
        dt = dt.replace(minute=0, second=0, microsecond=0)
        d = {
            'action_type': request.data.get('action_type'),
            'start_time': dt,
            'decision': request.data.get('decision'),
            'cycle': current_cycle,
        }
        a = ActionSerializer().create(d)
        return response.Response(ActionSerializer(instance=a).data)


class BoxViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
