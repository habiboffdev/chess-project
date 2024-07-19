from rest_framework import serializers
from .models import AvailablePlayer, Match

class AvailablePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlayer
        fields = ['is_available']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['result_reported','winner']
