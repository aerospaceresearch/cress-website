from rest_framework import serializers


class AXSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    text = serializers.CharField()
    text_as_html = serializers.CharField()
    uid = serializers.CharField()
    collection_name = serializers.CharField()
    collection_id = serializers.IntegerField()
    text_modified = serializers.CharField()
    language = serializers.CharField()
