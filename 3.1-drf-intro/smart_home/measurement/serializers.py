from rest_framework import serializers

from .models import Sensor, Measurement


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'date', 'image', 'sensor']


class SensorDetailSerializer(serializers.ModelSerializer):
    sensor = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'sensor']

    def get_measurements(self, obj):
        measurements = obj.sensor.all()
        return MeasurementSerializer(measurements, many=True).data
