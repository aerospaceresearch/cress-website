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
            cycle_list = range(3, Cycle.objects.order_by("-pk").first().pk)
        for cycle in cycle_list:
            with open("/opt/code/export/cycle_{}_photo.list".format(cycle), "w") as fp:
                fp.write('"id";"filename"\n')
                for element in qs.filter(cycle_id=cycle).order_by('created'):
                    if element.photo:
                        fp.write('{};"{}"\n'.format(element.pk, element.photo.name))
