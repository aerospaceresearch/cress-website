from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import HomePageView, latest_photo


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^latest_photo/$', latest_photo, name='photojson'),
    url(r'^about/$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^legal/$', TemplateView.as_view(template_name='main/legal.html'), name='legal'),
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
