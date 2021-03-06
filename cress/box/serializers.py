import datetime
from rest_framework import serializers
from .models import Photo, Cycle, Sensor, Box, Action, Plant, Plot
from django.utils import timezone


class SecondsFromStartMixin():
    def get_seconds_from_cycle_start(self, obj):
        delta = (obj.created - obj.cycle.created)
        return (delta.days * 3600 * 24) + delta.seconds


class PhotoSerializer(SecondsFromStartMixin, serializers.HyperlinkedModelSerializer):
    box = serializers.IntegerField(write_only=True)
    seconds_from_cycle_start = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'box', 'created', 'seconds_from_cycle_start', 'removed')

    def create(self, validated_data):
        box = validated_data.pop('box')
        validated_data['owner'] = self.context['request'].user
        validated_data['cycle'] = Cycle.objects.filter(active=True).filter(box__id=box).order_by('-modified').first()
        return super().create(validated_data)


class PlotSerializer(serializers.HyperlinkedModelSerializer):
    cycle_id = serializers.IntegerField()

    class Meta:
        model = Plot
        fields = ('id', 'plot', 'cycle_id', 'created', 'description')

    def create(self, validated_data):
        cycle_id = validated_data.pop('cycle_id')
        cycle = Cycle.objects.filter(pk=cycle_id).first()
        validated_data['cycle'] = cycle
        # magic here, because the api should always be POST
        existing = Plot.objects.filter(cycle=cycle, description=validated_data['description']).first()
        if existing:
            existing.plot.delete(save=False)
            existing.plot = validated_data['plot']
            existing.save()
            return existing
        return super().create(validated_data)


class SensorCreateSerializer(serializers.HyperlinkedModelSerializer):
    box = serializers.IntegerField(write_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'box',
                  'sensor_type', 'value_type', 'description', 'position', 'unit', 'value')

    def create(self, validated_data):
        box = validated_data.pop('box')
        validated_data['cycle'] = Cycle.objects.filter(active=True).filter(box__id=box).order_by('-modified').first()
        return super().create(validated_data)


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('action_type', 'decision', 'start_time', 'cycle')
        extra_kwargs = {'cycle': {'write_only': True}}


class BoxSerializer(serializers.ModelSerializer):
    sensors = serializers.SerializerMethodField()
    defaults = serializers.SerializerMethodField()

    def get_defaults(self, obj):
        current_cycle = Cycle.objects.filter(active=True).filter(box__id=obj.pk).order_by('-modified').first()
        return {
            'water': current_cycle.water_start_level,
            'uv': current_cycle.uv_start_level,
        }

    def get_sensors(self, obj):
        current_cycle = Cycle.objects.filter(active=True).filter(box__id=obj.pk).order_by('-modified').first()
        time_threshold = timezone.now() - datetime.timedelta(minutes=6)
        sensor_list = current_cycle.sensor.filter(created__gt=time_threshold).order_by('-modified')
        return SensorSerializer(sensor_list, many=True).data

    class Meta:
        model = Box
        fields = ('id', 'sensors', 'defaults')


class BoxActionSerializer(serializers.HyperlinkedModelSerializer):
    action = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ('id', 'action')

    def get_action(self, obj):
        dt = timezone.now()
        dt = dt.replace(minute=0, second=0, microsecond=0)
        current_cycle = Cycle.objects.filter(active=True).filter(box__id=obj.pk).order_by('-modified').first()
        qs_action = Action.objects.filter(cycle=current_cycle).filter(start_time__gte=dt)
        if not qs_action:
            dt_prev = dt - datetime.timedelta(hours=1)
            prev_actions = Action.objects.filter(cycle=current_cycle).filter(start_time__gte=dt_prev)

            # create actions
            actions = []
            for action, _ in Action.ACTION_CHOICES:
                p = prev_actions.filter(action_type=action).order_by('-modified').first()
                if p:
                    p = p.decision
                else:
                    if action == 'UV light':
                        p = current_cycle.uv_start_level
                    elif action == 'Water':
                        p = current_cycle.water_start_level
                d = {
                    'action_type': action,
                    'start_time': dt,
                    'decision': p,
                    'cycle': current_cycle,
                }
                actions.append(ActionSerializer().create(d))
        else:
            actions = [qs_action.filter(action_type=action).order_by('-modified').first() for action, _ in Action.ACTION_CHOICES]
        return [ActionSerializer(instance=i).data for i in actions]


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ('id', 'name_en', 'name_la', 'wikipedia_en')


class CycleSerializer(serializers.ModelSerializer):
    plant = PlantSerializer()

    class Meta:
        model = Cycle
        fields = ('id', 'start_date', 'name', 'soil', 'plant', 'box')


class SensorSerializer(SecondsFromStartMixin, serializers.ModelSerializer):
    seconds_from_cycle_start = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ('id', 'cycle', 'sensor_type', 'value_type', 'description',
                  'position', 'unit', 'value', 'created', 'seconds_from_cycle_start')
