import json
import datetime

from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from box.models import Box, Cycle, Photo, Sensor, Report, Plot
from ax.models import AxText


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        cycle_list = Cycle.objects.filter(box__in=Box.objects.filter(pk__in=[1,2,4])).order_by("-created").select_related()
        cycle_active = cycle_list.filter(active=True)
        context["cycle_list"] = cycle_list
        context["cycle_active"] = cycle_active
        context["boxes"] = Box.objects.filter(id__in=[1,2,4])
        photos = []
        for cycle in cycle_active:
            p = Photo.objects.exclude(removed=True).filter(cycle=cycle).order_by('-created').first()
            if p:
                photos.append(p)
        context['photos'] = photos
        # photos = Photo.objects.filter(cycle__box=3).order_by('-created').first()
        # if photos:
        #     context['outside_image'] = photos
        context['generated_text'] = AxText.objects.exclude(_text='').order_by('-modified').first()._text
        return context


class CycleView(TemplateView):

    template_name = "main/cycle.html"

    def get_context_data(self, **kwargs):
        context = super(CycleView, self).get_context_data(**kwargs)
        cycle = Cycle.objects.filter(id=self.kwargs['cycle']).select_related().first()
        if not cycle:
            from django.http import Http404
            raise Http404("Cycle does not exist")
        context["cycle"] = cycle
        context["report"] = Report.objects.filter(cycle=cycle).first()
        photos = Photo.objects.exclude(removed=True).filter(cycle=cycle).order_by('-created')
        sensors = Sensor.objects.filter(cycle=cycle).select_related().order_by('-created')
        context["cycle_prev"] = Cycle.objects.filter(box=cycle.box).filter(id__lt=cycle.id).order_by('-created').first()
        context["cycle_next"] = Cycle.objects.filter(box=cycle.box).filter(id__gt=cycle.id).order_by('created').first()
        context["boxes"] = Box.objects.filter(id__in=[1,2,4])
        photo = photos.first()
        if photo:
            context['image'] = photo
            days = abs((photos.last().created - photo.created).days)
            context['older_images'] = []
            for day in range(1, days + 1):
                time_threshold = photo.created - datetime.timedelta(days=day)
                img = photos.filter(created__lt=time_threshold).first()
                if img:
                    context['older_images'].append(img)
        context['plots'] = Plot.objects.filter(cycle=cycle).order_by('created')
        if sensors.first():
            if cycle.active:
                if cycle.box.id == 1:
                    count_of_sensors = 8
                if cycle.box.id == 2:
                    count_of_sensors = 6
                if cycle.box.id == 4:
                    count_of_sensors = 7
                context['sensor_list'] = sensors[:count_of_sensors]
            chart_data = sensors.filter(sensor_type="DHT22", value_type='humidity')
            # only one value per hour.
            chart_data = chart_data.filter(created__minute=chart_data.first().created.minute).order_by('created')
            context['chart_data'] = chart_data.select_related()
        return context


def latest_photo(request):
    photo = Photo.objects.exclude(removed=True).order_by('-created').first()
    if photo:
        return HttpResponse(json.dumps({
            'url': photo.photo.url,
            'created': str(photo.created)
        }))
    return HttpResponse("{}")
