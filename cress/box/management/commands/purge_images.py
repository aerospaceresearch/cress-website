# coding=utf-8
import datetime
import os.path

from django.core.management import BaseCommand


def delete_file(obj):
    if obj.image and os.path.isfile(obj.image.path):
        os.remove(obj.image.path)
        obj.purged = True
        obj.save()
        return 1
    return 0


class Command(BaseCommand):

    help = "Reduce number of images on local harddrive"

    def handle(self, *args, **options):
        from box.models import Photo

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        count = 0
        excludes_minutes = [59, 0, 1]
        for element in Photo.objects.exclude(created__gte=yesterday).exclude(created__minute__in=excludes_minutes):
            count += delete_file(element)
        if count:
            msg = "%s images were successfully purged." % count
        else:
            msg = "No images were purged."
        print(msg)
