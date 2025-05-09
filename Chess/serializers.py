from rest_framework import serializers
from .models import AvailablePlayer, Match, Tournament, TournamentParticipant, TournamentMatch
from Users.serializers import UserInfoSerializer
class AvailablePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlayer
        fields = ['is_available']

class MatchSerializer(serializers.ModelSerializer):
    # player1 field is not required
    player1 = serializers.StringRelatedField()
    player2 = serializers.StringRelatedField()
    class Meta:
        model = Match
        fields = "__all__"
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentParticipantSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()
    tournament = serializers.StringRelatedField()
    class Meta:
        model = TournamentParticipant
        fields = '__all__'
        
class TournamentMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatch
        fields = ['id', 'round', 'player1', 'player2', 'winner', 'draw']

class TournamentLeaderboardSerializer(serializers.ModelSerializer):
    player =  UserInfoSerializer()
    class Meta:
        model = TournamentParticipant
        fields = ['player', 'score']


class TournamentMatchDetailSerializer(serializers.ModelSerializer):
    player1 = UserInfoSerializer()
    player2 = UserInfoSerializer()
    round = serializers.StringRelatedField()

    class Meta:
        model = TournamentMatch
        fields = ['id', 'round', 'player1', 'player2', 'winner', 'draw']