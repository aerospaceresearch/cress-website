from rest_framework import serializers


class AXSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    text = serializers.CharField()
    html = serializers.CharField()
    html_axite = serializers.CharField()
    uid = serializers.CharField()
    collection_name = serializers.CharField()
    collection_id = serializers.IntegerField()
    text_modified = serializers.CharField()
    language = serializers.CharField()
