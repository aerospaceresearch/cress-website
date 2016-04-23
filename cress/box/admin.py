from django.contrib import admin
from .models import Box, Cycle, Photo


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
