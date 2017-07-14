from django.contrib import admin
from .models import AxText


@admin.register(AxText)
class AxTextAdmin(admin.ModelAdmin):
    list_display = ('pk', '_text', 'created')
