from django.views.generic.base import TemplateView

from box.models import Photo


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        if Photo.objects.order_by('-created').first():
            context['image'] = Photo.objects.order_by('-created').first().image
        return context
