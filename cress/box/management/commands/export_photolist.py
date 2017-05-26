# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Exports csv files with all photos for each cycle"

    def add_arguments(self, parser):
        parser.add_argument('--cycle', type=int, default=0)

    def handle(self, *args, **options):
        from box.models import Cycle, Photo

        cycle = options.get('cycle')
        qs = Photo.objects.all()
        if cycle:
            cycle_list = [cycle]
        else:
            cycle_list = list(Cycle.objects.exclude(pk=9).exclude(active=True).order_by("pk").values_list('pk', flat=True))
        for cycle in cycle_list:
            fn = "/opt/code/export/cycle_{}_photo.list".format(cycle)
            print(fn)
            with open(fn, "w") as fp:
                fp.write('"id";"box";"box_cycle";"filename"\n')
                for element in qs.filter(cycle_id=cycle).order_by('created'):
                    if element.photo:
                        box = '{:d}'.format(int(element.cycle.box.description.split(' ')[-1]))
                        box_cycle = element.cycle.name.split(' ')[-1]
                        fp.write('{};{};{};"{}"\n'.format(element.pk, box, box_cycle, element.photo.name))
