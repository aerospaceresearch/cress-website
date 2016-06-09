# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "List all files of a specific cycle"

    def add_arguments(self, parser):
        parser.add_argument('--cycle', type=int)

    def handle(self, *args, **options):
        from box.models import Photo

        cycle = options.get('cycle')
        for element in Photo.objects.filter(cycle_id=cycle).order_by('created'):
            print(element.image.name.split('/')[-1])
