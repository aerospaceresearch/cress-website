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
        photos = Photo.objects.filter(cycle=cycle_active.first()).order_by('-created')
        sensors = Sensor.objects.filter(cycle=cycle_active.first()).order_by('-created')
        if photos.first():
            context['image'] = photos.first()
            days = abs((photos.last().created - photos.first().created).days)
            context['older_images'] = []
            for day in range(1, days + 1):
                time_threshold = photos.first().created - datetime.timedelta(days=day)
                context['older_images'].append(photos.filter(created__lt=time_threshold).first())
        if sensors.first():
            context['sensors'] = sensors[:7]
        return context


def latest_photo(request):
    photo = Photo.objects.order_by('-created').first()
    if photo:
        return HttpResponse(json.dumps({
            'url': photo.image.url,
            'created': str(photo.created)
        }))
    return HttpResponse("{}")
