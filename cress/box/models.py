from django.db import models
from django_extensions.db.models import TimeStampedModel


class Box(TimeStampedModel):
    cress_space_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{s.description}".format(s=self)


class Cycle(TimeStampedModel):
    start_date = models.DateTimeField()
    box = models.ForeignKey('Box', related_name='box')
    plant = models.TextField()


class Photo(TimeStampedModel):
    image = models.ImageField(upload_to='photos', max_length=254)
    owner = models.ForeignKey('auth.User', related_name='image')
    cycle = models.ForeignKey('Cycle', related_name='cycle')
