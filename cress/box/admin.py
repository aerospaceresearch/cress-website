import datetime
import os.path
from django.contrib import admin
from .models import Box, Cycle, Photo, Sensor, Action


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('description', 'location')


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('box', 'name', 'plant', 'start_date', 'active')


def delete_file(obj):
    if obj.image and os.path.isfile(obj.image.path):
        os.remove(obj.image.path)
        obj.purged = True
        obj.save()
        return 1
    return 0


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'image', 'cycle', 'created', 'not_purged')
    list_filter = ('cycle', 'purged')
    actions = ('purge_images', 'purge_images_half')

    def not_purged(self, obj):
        return not obj.purged
    not_purged.boolean = True

    def purge_images(self, request, queryset):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        count = 0
        for element in queryset.exclude(created__gte=yesterday):
            count += delete_file(element)
        if count:
            msg = "%s images were successfully purged." % count
        else:
            msg = "No images were purged."
        self.message_user(request, msg)
    purge_images.short_description = "Purge selected images if older than yesterday"

    def purge_images_half(self, request, queryset):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        count = 0
        for element in queryset.exclude(created__gte=yesterday).exclude(created__minute__in=[i for i in range(0, 60, 10)]):
            count += delete_file(element)
        if count:
            msg = "%s images were successfully purged." % count
        else:
            msg = "No images were purged."
        self.message_user(request, msg)
    purge_images_half.short_description = "Purge selected images if older than yesterday and not divisable on 10."


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value_type', 'position', 'unit', 'value', 'cycle', 'created')
    list_filter = ('sensor_type', 'value_type', 'position', 'unit', 'cycle')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'cycle', 'decision', 'start_time')
    list_filter = ('action_type', 'cycle')
