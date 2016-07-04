from django.db import models
from django_extensions.db.models import TimeStampedModel


class Box(TimeStampedModel):
    cress_space_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{s.description}".format(s=self)

    class Meta:
        verbose_name_plural = 'Boxes'


class Cycle(TimeStampedModel):
    start_date = models.DateTimeField()
    plant = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="")
    box = models.ForeignKey('Box', related_name='cycle')
    water_start_level = models.IntegerField(default=50, help_text="start water level in percent")
    uv_start_level = models.IntegerField(default=50, help_text="start uv level in percent")
    hourly_step = models.IntegerField(default=5, help_text="change per hour in percent")
    active = models.NullBooleanField()

    def __str__(self):
        return "{s.box} {s.start_date}".format(s=self)


class Photo(TimeStampedModel):
    image = models.ImageField(upload_to='photos', max_length=254)
    owner = models.ForeignKey('auth.User', related_name='image')
    cycle = models.ForeignKey('Cycle', related_name='photo')
    purged = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{s.image}".format(s=self)


class Sensor(TimeStampedModel):
    sensor_type = models.CharField(max_length=100,
                                   choices=(('DHT22', 'DHT22'),
                                            ('photoresistor', 'photoresistor'),
                                            ('photodiode', 'photodiode'),
                                            ('FC28', 'FC28'),   # watermark
                                        ))
    value_type = models.CharField(max_length=100,
                                  choices=(('temperature', 'temperature [DHT22]'),
                                           ('humidity', 'humidity [DHT22]'),
                                           ('watermark', 'water mark'),
                                           ('brightness', 'brightness'),
                                       ))
    description = models.TextField(null=True, blank=True)
    position = models.CharField(max_length=100,
                                choices=(('inside', 'inside'),
                                         ('outside', 'outside'), ))
    unit = models.CharField(max_length=100,
                            choices=(('°C', '°C'),
                                     ('%', '%'),
                                     ('Pa', 'Pa'),
                                     ('-', '-'),
                                 ))
    value = models.CharField(max_length=255)
    cycle = models.ForeignKey('Cycle', related_name='sensor')

    def __str__(self):
        return "{s.sensor_type} {s.position}".format(s=self)


class Action(TimeStampedModel):
    ACTION_CHOICES = (
        ('UV light', 'UV light'),
        ('Water', 'Water'),
    )

    action_type = models.CharField(max_length=100,
                                   choices=ACTION_CHOICES)
    cycle = models.ForeignKey('Cycle', related_name='action')
    decision = models.IntegerField()
    start_time = models.DateTimeField()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{s.action_type} {s.cycle}".format(s=self)
