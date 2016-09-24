import datetime
import os.path
from django.contrib import admin
from .models import Action, Box, Cycle, Photo, Report, Sensor


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
    actions = ('purge_images', 'purge_images_most')
    readonly_fields = ('modified', 'created')

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

    def purge_images_most(self, request, queryset):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        count = 0
        excludes_minutes = [59, 0, 1, 29, 30, 31]
        for element in queryset.exclude(created__gte=yesterday).exclude(created__minute__in=excludes_minutes):
            count += delete_file(element)
        if count:
            msg = "%s images were successfully purged." % count
        else:
            msg = "No images were purged."
        self.message_user(request, msg)
    purge_images_most.short_description = "Purge selected images if older than yesterday and on full/half hour."


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
