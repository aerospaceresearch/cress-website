from django.contrib import admin
from .models import Box, Cycle, Photo, Sensor, Action


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('description', 'location')


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('box', 'plant', 'start_date')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'cycle', 'created')


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value_type', 'position', 'unit', 'value', 'cycle', 'created')
    list_filter = ('sensor_type', 'value_type', 'position', 'unit', 'cycle')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'cycle', 'decision', 'start_time')
    list_filter = ('action_type', 'cycle')
