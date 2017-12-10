# coding: utf-8
import os.path

import markdown
from PIL import Image
from io import BytesIO

from django.db import models
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel
from django.core.files.uploadedfile import SimpleUploadedFile


class Box(TimeStampedModel):
    cress_space_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{s.description}".format(s=self)

    class Meta:
        ordering = ('description', )
        verbose_name_plural = 'Boxes'


class Cycle(TimeStampedModel):
    start_date = models.DateTimeField()
    plant = models.ForeignKey('Plant', on_delete=models.PROTECT)
    name = models.CharField(max_length=255, default="")
    box = models.ForeignKey('Box', related_name='cycle', on_delete=models.PROTECT)
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
                                ('potting soil', 'potting soil'),
                            ))
    adc_used = models.CharField(max_length=255,
                                blank=True,
                                default='adc16',
                                choices=(
                                    ('adc10', 'Arduino'),
                                    ('adc16', 'ADS1x15'),
                                ))

    class Meta:
        ordering = ('-created', )

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('cycle', kwargs={'cycle': self.id})

    def __str__(self):
        return "{s.box} - {s.name} - {start_date}".format(s=self, start_date=self.start_date.date())

    # def save(self, *args, **kwargs):
    #     if self.active:
    #         Cycle.objects.filter(box=self.box).filter(active=True).update(active=False)
    #     return super().save(*args, **kwargs)


def image_directory(instance, filename):
    return 'photo/c{0}/{1}'.format(instance.cycle.pk, filename)


class Photo(TimeStampedModel):
    photo = models.ImageField(upload_to=image_directory, max_length=254, null=True, blank=True)
    thumbnail = models.ImageField(max_length=254, null=True, blank=True)
    owner = models.ForeignKey('auth.User', related_name='image', on_delete=models.PROTECT)
    cycle = models.ForeignKey('Cycle', related_name='photo', on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{s.photo}".format(s=self)

    def create_thumbnail(self):
        if not self.photo:
            return

        # Open original photo which we want to thumbnail using PIL's Image
        try:
            image = Image.open(BytesIO(self.photo.read()))
        except FileNotFoundError:
            return

        image.thumbnail((430, 320), Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, 'jpeg')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.photo.name)[-1],
                                 temp_handle.read(), content_type='image/jpeg')
        self.thumbnail.save('thumbnail/c{0}/{1}'.format(self.cycle.pk,
                                                        os.path.split(self.photo.name)[-1]),
                            suf, save=False)

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super().save(*args, **kwargs)


class Sensor(TimeStampedModel):
    sensor_type = models.CharField(max_length=100,
                                   choices=(('DHT22', 'DHT22'),
                                            ('photoresistor', 'photoresistor'),
                                            ('photodiode', 'photodiode'),
                                            ('FC28', 'FC28'),   # watermark
                                            ('capacitive-moisture', 'Capacitive Moisture'),   # watermark
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
    cycle = models.ForeignKey('Cycle', related_name='sensor', on_delete=models.PROTECT)

    def __str__(self):
        return "{s.sensor_type} {s.position}".format(s=self)


class Action(TimeStampedModel):
    ACTION_CHOICES = (
        ('UV light', 'UV light'),
        ('Water', 'Water'),
    )

    action_type = models.CharField(max_length=100,
                                   choices=ACTION_CHOICES)
    cycle = models.ForeignKey('Cycle', related_name='action', on_delete=models.PROTECT)
    decision = models.IntegerField()
    start_time = models.DateTimeField()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return "{s.action_type} {s.cycle}".format(s=self)


class Report(TimeStampedModel):
    cycle = models.OneToOneField('Cycle', related_name='report', on_delete=models.PROTECT)
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

    class Meta:
        ordering = ('name_en', )

    def __str__(self):
        return "{s.name_en} ({s.name_la})".format(s=self)


def plot_image_directory(instance, filename):
    return 'plot/c{0}/{1}'.format(instance.cycle.pk, filename)


class Plot(TimeStampedModel):
    plot = models.ImageField(upload_to=plot_image_directory, max_length=254, null=True, blank=True)
    description = models.CharField(max_length=255)
    cycle = models.ForeignKey('Cycle', related_name='plot', on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created', )
        unique_together = (('cycle', 'description'), )

    def __str__(self):
        return "{s.plot} {s.description}".format(s=self)
