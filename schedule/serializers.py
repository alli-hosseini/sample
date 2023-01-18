from rest_framework import serializers


class CreateScheduleSerializer(serializers.Serializer):
    vendor_id = serializers.CharField(max_length=255)
    unit = serializers.CharField(max_length=50)
    value = serializers.IntegerField()
    categories = serializers.ListField(child=serializers.DictField())
