import datetime
from rest_framework import serializers
from .models import Photo, Cycle, Sensor, Box, Action
from django.utils import timezone


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    box = serializers.IntegerField(write_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'image', 'box')

    def create(self, validated_data):
        box = validated_data.pop('box')
        validated_data['owner'] = self.context['request'].user
        validated_data['cycle'] = Cycle.objects.filter(active=True).filter(box__id=box).order_by('-modified').first()
        return super().create(validated_data)


class SensorSerializer(serializers.HyperlinkedModelSerializer):
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
        # for now only one sensor_type
        sensor_list = []
        # FIXME: add code to get from all sensors newest value
        sensor_list.append(current_cycle.sensor.filter(sensor_type='FC28', value_type="watermark", position="inside").order_by('-modified').first())
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
        actions = Action.objects.filter(cycle=current_cycle).filter(start_time__gte=dt)
        if not actions:
            dt_prev = dt - datetime.timedelta(hours=1)
            prev_actions = Action.objects.filter(cycle=current_cycle).filter(start_time__gte=dt_prev)

            # create actions
            actions = []
            for action, _ in Action.ACTION_CHOICES:
                p = prev_actions.filter(action_type=action).first()
                if p:
                    p = p.decision
                else:
                    if action == 'UV light':
                        p = current_cycle.uv_start_level
                    elif action == 'Water':
                        p = current_cycle.water_start_level
                # FIXME: change decision according to vote
                d = {
                    'action_type': action,
                    'start_time': dt,
                    'decision': p,
                    'cycle': current_cycle,
                }
                actions.append(ActionSerializer().create(d))
        return [ActionSerializer(instance=i).data for i in actions]
