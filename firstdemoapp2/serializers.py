from rest_framework import serializers
from .models import SensorData,Farmer,todouser,daysandassignments,arduinodata,SportsDailyActivity,SportsDailyActivityImages,SportsNotificationToken


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

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


class SportsNotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsNotificationToken
        fields = ['username', 'device_token']


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'
