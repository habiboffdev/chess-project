from rest_framework import serializers
from .models import AvailablePlayer, Match, Tournament, TournamentParticipant, TournamentMatch

class AvailablePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlayer
        fields = ['is_available']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['result_reported','winner']
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipant
        fields = '__all__'
        
class TournamentMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatch
        fields = ['id', 'round', 'player1', 'player2', 'winner', 'draw']

class TournamentLeaderboardSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()

    class Meta:
        model = TournamentParticipant
        fields = ['player', 'score']


class TournamentMatchDetailSerializer(serializers.ModelSerializer):
    player1 = serializers.StringRelatedField()
    player2 = serializers.StringRelatedField()
    round = serializers.StringRelatedField()

    class Meta:
        model = TournamentMatch
        fields = ['id', 'round', 'player1', 'player2', 'winner', 'draw']