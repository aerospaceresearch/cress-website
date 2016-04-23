from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('main.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('box.urls')),
]
