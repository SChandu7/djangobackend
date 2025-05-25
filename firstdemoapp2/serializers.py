from rest_framework import serializers
from .models import todouser

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = todouser
        fields = ['userid', 'userdata', 'days', 'assignments']
