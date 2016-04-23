from django.contrib import admin
from .models import Box, Cycle, Photo


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('description', 'location')


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('box', 'plant', 'start_date')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'cycle', 'created')
