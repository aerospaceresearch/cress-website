# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Generate a new text via AX-Semantics SaaS."

    def handle(self, *args, **options):
        from ax.models import AxText
        from box.models import Cycle

        # FIXME: fetch some data
        data = {
            # cycle 9 is the mounted camera and no real box
            'active_boxes_count': Cycle.objects.exclude(pk=9).filter(active=True).count(),
        }

        obj = AxText.objects.create()
        data['uid'] = obj.pk
        obj.data_sent = data
        obj.order_text()
