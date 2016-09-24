from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import HomePageView, CycleView, latest_photo


urlpatterns = [
    url(r'^cycle/(?P<cycle>[0-9]+)/$', CycleView.as_view(), name='cycle'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^latest_photo/$', latest_photo, name='photojson'),
    url(r'^about/$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^legal/$', TemplateView.as_view(template_name='main/legal.html'), name='legal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
