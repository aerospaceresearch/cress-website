from django.utils import timezone
from rest_framework import (
    mixins, viewsets, parsers, permissions, response, pagination
)

from .models import Photo, Sensor, Box, Cycle, Plot
from .serializers import (
    BoxActionSerializer,
    BoxSerializer,
    CycleSerializer,
    PhotoSerializer,
    PlotSerializer,
    SensorCreateSerializer,
    SensorSerializer,
)


class TenPerPagePagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 1000
    page_size_query_param = 'page_size'


class PhotoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)
    pagination_class = TenPerPagePagination

    def list(self, request, *args, **kwargs):
        self.serializer_class = PhotoSerializer
        if self.request.GET.get('cycle'):
            try:
                self.queryset = Photo.objects.filter(cycle_id=int(self.request.GET.get('cycle')))
            except ValueError:
                pass
        return super().list(request, *args, **kwargs)


class PlotViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Plot.objects.none()
    serializer_class = PlotSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)
    pagination_class = TenPerPagePagination

    def list(self, request, *args, **kwargs):
        self.serializer_class = PhotoSerializer
        if self.request.GET.get('cycle'):
            try:
                self.queryset = Plot.objects.filter(cycle_id=int(self.request.GET.get('cycle')))
            except ValueError:
                pass
        return super().list(request, *args, **kwargs)


class SensorViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sensor.objects.none()
    serializer_class = SensorCreateSerializer
    pagination_class = TenPerPagePagination

    def list(self, request, *args, **kwargs):
        self.serializer_class = SensorSerializer
        if self.request.GET.get('cycle'):
            try:
                self.queryset = Sensor.objects.filter(cycle_id=int(self.request.GET.get('cycle')))
            except ValueError:
                pass
        return super().list(request, *args, **kwargs)


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


class CycleViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer
