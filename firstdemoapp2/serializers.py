from rest_framework import serializers
from .models import todouser,daysandassignments,arduinodata,SportsDailyActivity,SportsDailyActivityImages

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = todouser
        fields = ['userid', 'userdata', 'days', 'assignments']

class DisplayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = daysandassignments
        fields = ['days', 'assignments', 'description']
class ArduinoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = arduinodata
        fields = ['time', 'result']


class SportsDailyActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsDailyActivityImages
        fields = ['image_url']


class SportsDailyActivitySerializer(serializers.ModelSerializer):
    images = SportsDailyActivityImageSerializer(many=True, read_only=True)

    class Meta:
        model = SportsDailyActivity
        fields = ['id', 'school', 'date', 'time', 'pt_name', 'activity_type', 'game_name', 'images']


