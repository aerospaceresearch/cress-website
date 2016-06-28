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


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'image', 'cycle', 'created', 'not_purged')
    list_filter = ('cycle', 'purged')
    actions = ('purge_images', )

    def not_purged(self, obj):
        return not obj.purged
    not_purged.boolean = True

    def purge_images(self, request, queryset):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        count = 0
        for element in queryset.exclude(created__gte=yesterday):
            if element.image:
                if os.path.isfile(element.image.path):
                    os.remove(element.image.path)
                    element.purged = True
                    element.save()
                    count += 1
        self.message_user(request, "%s images were successfully purged." % count)
    purge_images.short_description = "Purge selected images if older than yesterday"


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value_type', 'position', 'unit', 'value', 'cycle', 'created')
    list_filter = ('sensor_type', 'value_type', 'position', 'unit', 'cycle')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'cycle', 'decision', 'start_time')
    list_filter = ('action_type', 'cycle')
