# Generated by Django 2.0 on 2017-12-10 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0031_auto_20171202_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('DHT22', 'DHT22'), ('photoresistor', 'photoresistor'), ('photodiode', 'photodiode'), ('FC28', 'FC28'), ('capacitive-moisture', 'Capacitive Moisture')], max_length=100),
        ),
    ]
