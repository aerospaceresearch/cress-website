from django.contrib import admin
from .models import AxText, AxTiming


@admin.register(AxText)
class AxTextAdmin(admin.ModelAdmin):
    list_display = ('pk', '_text', 'created')


@admin.register(AxTiming)
class AxTimingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'axtext', 'axite_id', 'full_generation_roundtrip', 'created')
    list_filter = ('return_code', )
    raw_id_fields = ('axtext', )
