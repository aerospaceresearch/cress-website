import datetime
import os.path
from django.contrib import admin
from .models import Action, Box, Cycle, Photo, Report, Sensor, Plant, Plot


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('description', 'location')


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('box', 'name', 'plant', 'start_date', 'active', 'soil', 'adc_used')
    list_filter = ('box', 'plant', 'soil', 'adc_used')


def delete_file(obj):
    if obj.image and os.path.isfile(obj.image.path):
        os.remove(obj.image.path)
        obj.save()
        return 1
    return 0


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'photo', 'cycle', 'created')
    list_filter = ('cycle', )
    readonly_fields = ('modified', 'created')


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('plot', 'cycle', 'created', 'description')
    list_filter = ('cycle', )
    readonly_fields = ('modified', 'created')


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value_type', 'position', 'unit', 'value', 'cycle', 'created')
    list_filter = ('sensor_type', 'value_type', 'position', 'unit', 'cycle')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'cycle', 'decision', 'start_time', 'created')
    list_filter = ('action_type', 'cycle')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('cycle', 'created', 'text')
    list_filter = ('cycle__box', 'cycle',)
    readonly_fields = ('modified', 'created')


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_la')
    readonly_fields = ('modified', 'created')
