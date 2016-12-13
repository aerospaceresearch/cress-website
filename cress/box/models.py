# coding: utf-8

import markdown
from django.db import models
from django.utils.safestring import mark_safe
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
    plant = models.ForeignKey('Plant')
    name = models.CharField(max_length=255, default="")
    box = models.ForeignKey('Box', related_name='cycle')
    water_start_level = models.IntegerField(default=50, help_text="start water level in percent")
    uv_start_level = models.IntegerField(default=0, help_text="start uv level in percent")
    hourly_step = models.IntegerField(default=5, help_text="change per hour in percent")
    active = models.NullBooleanField()
    soil = models.CharField(max_length=255,
                            null=True, blank=True,
                            choices=(
                                ('cotton wool (medical)', 'cotton wool (medical)'),
                                ('cotton wool (cosmetics)', 'cotton wool (cosmetics)'),
                                ('red clay (Seramis)', 'red clay (Seramis)'),
                                ('orchid soil (Orchideenerde)', 'orchid soil (Orchideenerde)'),
                            ))

    class Meta:
        ordering = ('-created', )

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('cycle', kwargs={'cycle': self.id})

    def __str__(self):
        return "{s.box} - {s.name} - {start_date}".format(s=self, start_date=self.start_date.date())

    def save(self, *args, **kwargs):
        if self.active:
            Cycle.objects.filter(box=self.box).filter(active=True).update(active=False)
        super().save(*args, **kwargs)


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


class Report(TimeStampedModel):
    cycle = models.OneToOneField('Cycle', related_name='report')
    text = models.TextField()

    class Meta:
        ordering = ('cycle', )

    @property
    def text_as_html(self):
        return mark_safe(markdown.markdown(self.text))

    def __str__(self):
        return "{s.text}".format(s=self)


class Plant(TimeStampedModel):
    name_en = models.CharField(max_length=255)
    name_la = models.CharField(max_length=255)
    wikipedia_en = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{s.name_en} ({s.name_la})".format(s=self)
