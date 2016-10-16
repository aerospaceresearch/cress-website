import json
import datetime

from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from box.models import Box, Cycle, Photo, Sensor, Report


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        cycle_list = Cycle.objects.filter(box__in=Box.objects.filter(pk__in=[1,2,4])).order_by("-created")
        cycle_active = cycle_list.filter(active=True)
        context["cycle_list"] = cycle_list
        context["cycle_active"] = cycle_active
        context["boxes"] = Box.objects.filter(id__in=[1,2])
        photos = []
        for cycle in cycle_active:
            p = Photo.objects.exclude(purged=True).filter(cycle=cycle).order_by('-created').first()
            if p:
                photos.append(p)
        context['photos'] = photos
        photos = Photo.objects.exclude(purged=True).filter(cycle__box=3).order_by('-created')
        if photos:
            context['outside_image'] = photos.first()
        return context


class CycleView(TemplateView):

    template_name = "main/cycle.html"

    def get_context_data(self, **kwargs):
        context = super(CycleView, self).get_context_data(**kwargs)
        cycle = Cycle.objects.filter(id=self.kwargs['cycle'])
        if not cycle:
            from django.http import Http404
            raise Http404("Cycle does not exist")
        cycle_active = cycle.first()
        context["cycle"] = cycle_active
        context["report"] = Report.objects.filter(cycle=cycle_active).first()
        photos = Photo.objects.exclude(purged=True).filter(cycle=cycle_active).order_by('-created')
        sensors = Sensor.objects.filter(cycle=cycle_active).order_by('-created')
        context["cycle_prev"] = Cycle.objects.filter(box=cycle_active.box).filter(id__lt=cycle_active.id).order_by('-created').first()
        context["cycle_next"] = Cycle.objects.filter(box=cycle_active.box).filter(id__gt=cycle_active.id).order_by('created').first()
        context["boxes"] = Box.objects.filter(id__in=[1,2,4])
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
            if cycle_active.active:
                context['sensor_list'] = sensors[:7]
            chart_data = sensors.filter(sensor_type="DHT22", value_type='humidity')
            # only one value per hour.
            chart_data = chart_data.filter(created__minute=chart_data.first().created.minute).order_by('created')
            context['chart_data'] = chart_data
        return context


def latest_photo(request):
    photo = Photo.objects.order_by('-created').first()
    if photo:
        return HttpResponse(json.dumps({
            'url': photo.image.url,
            'created': str(photo.created)
        }))
    return HttpResponse("{}")
