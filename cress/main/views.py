import json

from django.views.generic.base import TemplateView
from django.http import HttpResponse

from box.models import Photo, Sensor


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        if Photo.objects.order_by('-created').first():
            context['image'] = Photo.objects.order_by('-created').first()
        if Sensor.objects.order_by('-created').first():
            context['sensors'] = Sensor.objects.order_by('-created')[:4]
        return context


def latest_photo(request):
    photo = Photo.objects.order_by('-created').first()
    if photo:
        return HttpResponse(json.dumps({
            'url': photo.image.url
        }))
    return HttpResponse("{}")
