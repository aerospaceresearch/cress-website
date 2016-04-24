from django.db import models
from django_extensions.db.models import TimeStampedModel


class Vote(TimeStampedModel):
    user = models.ForeignKey('auth.User', related_name='vote')
    cycle = models.ForeignKey('box.Cycle', related_name='vote')
    action_type = models.CharField(max_length=100,
                                   choices=(('UV light', 'UV light'),
                                            ('Water', 'Water'),))
    decision = models.CharField(max_length=100,
                                choices=(('-1', 'less'),
                                         ('0', 'zero'),
                                         ('1', 'more'),))

    def __str__(self):
        return "{s.user} {s.cycle}".format(s=self)
