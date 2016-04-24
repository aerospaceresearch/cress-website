from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cycle', 'action_type', 'decision')
    list_filter = ('action_type', 'cycle')
