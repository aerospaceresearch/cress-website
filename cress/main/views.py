import json
import datetime

from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from box.models import Photo, Sensor, Cycle, Box


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        cycle_list = Cycle.objects.exclude(active__isnull=True).filter(box=Box.objects.get(pk=1)).order_by("created")
        cycle_active = cycle_list.filter(active=True)
        if str(self.request.GET.get('cycle')).isdigit():
            cycle_active = cycle_list.filter(pk=int(self.request.GET.get('cycle')))
            if not cycle_active:
                raise PermissionDenied()
        else:
            cycle_list = Cycle.objects.exclude(active__isnull=True).filter(box=Box.objects.get(pk=1)).order_by('start_date')
        context["cycle_list"] = cycle_list
        context["cycle_set"] = cycle_active.first().pk
        photos = Photo.objects.exclude(purged=True).filter(cycle=cycle_active.first()).order_by('-created')
        sensors = Sensor.objects.filter(cycle=cycle_active.first()).order_by('-created')
        if photos.first():
            photo = photos.first()
            context['image'] = photo
            days = abs((photos.last().created - photo.created).days)
            context['older_images'] = []
            for day in range(1, days + 1):
                time_threshold = photo.created - datetime.timedelta(days=day)
                img = photos.exclude(purged=True).filter(created__lt=time_threshold).first()
                if img:
                    context['older_images'].append(img)
        if sensors.first():
            if cycle_active.filter(active=True):
                context['sensor_list'] = sensors[:7]
            chart_data = sensors.filter(sensor_type="DHT22", value_type='humidity')
            # only one value per hour.
            chart_data = chart_data.filter(created__minute=chart_data.first().created.minute).order_by('created')
            context['chart_data'] = chart_data
        photos = Photo.objects.exclude(purged=True).filter(cycle__box=3).order_by('-created')
        if photos:
            context['outside_image'] = photos.first()
        return context


def latest_photo(request):
    photo = Photo.objects.order_by('-created').first()
    if photo:
        return HttpResponse(json.dumps({
            'url': photo.image.url,
            'created': str(photo.created)
        }))
    return HttpResponse("{}")
