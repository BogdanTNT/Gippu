from rest_framework import serializers
from Models import Robot

class CreateRobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('purpose')