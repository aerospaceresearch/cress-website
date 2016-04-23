from rest_framework import serializers
from .models import Photo, Cycle


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    box = serializers.IntegerField(write_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'image', 'box')

    def create(self, validated_data):
        box = validated_data.pop('box')
        validated_data['owner'] = self.context['request'].user
        validated_data['cycle'] = Cycle.objects.filter(box__id=box).order_by('modified').first()
        return super().create(validated_data)
