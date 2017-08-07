# coding=utf-8
import datetime
from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):

    help = "Push timings for past generations back to AX-Semantics."

    def handle(self, *args, **options):
        from ax.models import AxText, AxTiming
        from ax.utils import ax_timing_create, send_timings_to_report_api

        # all datasets modified in the last 60 minutes
        axtexts = AxText.objects.filter(modified__gte=(timezone.now() - datetime.timedelta(seconds=60 * 60)))
        for axtext in axtexts:
            ax_timing_create(axtext)
        for axtiming in AxTiming.objects.filter(return_code=None)
            axtiming.push_to_api()
