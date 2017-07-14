# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Generate a new text via AX-Semantics SaaS."

    def handle(self, *args, **options):
        from ax.models import AxText
        from box.models import Cycle, Plant, Sensor

        # cycle 9 is the mounted camera and no real box
        active_cycles = Cycle.objects.exclude(pk=9).filter(active=True)
        active_ids = active_cycles.values_list('id', flat=True)
        temp_outside = Sensor.objects.filter(cycle=9, value_type='temperature').order_by('-created').first()
        humidity_outside = Sensor.objects.filter(cycle=9, value_type='humidity').order_by('-created').first()

        data = {
            'active_boxes_count': active_cycles.count(),
            'plants': {},
            'outside_temperature': temp_outside.value,
            'outside_temperature_unit': temp_outside.unit,
            'outside_humidity': humidity_outside.value,
            'outside_humidity_unit': humidity_outside.unit,
        }
        for plant in Plant.objects.all():
            c = plant.cycle_set.filter(pk__in=active_ids)
            if c:
                data['plants'][plant.name_en] = {
                    'count': c.count()
                }

        obj = AxText.objects.create()
        data['uid'] = obj.pk
        obj.data_sent = data
        obj.save()
        obj.order_text()
