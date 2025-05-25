from rest_framework import serializers
from .models import todouser,daysandassignments

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = todouser
        fields = ['userid', 'userdata', 'days', 'assignments']

class DisplayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = daysandassignments
        fields = ['days', 'assignments', 'description']
