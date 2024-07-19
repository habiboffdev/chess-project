from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import AvailablePlayer, Match
from .serializers import AvailablePlayerSerializer, MatchSerializer
class CancelAvailabilityView(generics.GenericAPIView):
    queryset = AvailablePlayer.objects.all()
    serializer_class = AvailablePlayerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            available_player = AvailablePlayer.objects.get(player=request.user)
            available_player.is_available = False
            available_player.save()
            return Response({"detail": "Player availability cancelled."}, status=status.HTTP_200_OK)
        except AvailablePlayer.DoesNotExist:
            return Response({"detail": "Player not found or already not available."}, status=status.HTTP_400_BAD_REQUEST)

class SetAvailablePlayerView(generics.CreateAPIView):
    queryset = AvailablePlayer.objects.all()
    serializer_class = AvailablePlayerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user, is_available=True)

class MatchCreateView(generics.CreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        player1 = self.request.user

        try:
            available_player1 = AvailablePlayer.objects.get(player=player1, is_available=True)
        except AvailablePlayer.DoesNotExist:
            raise serializers.ValidationError("Player is not available for a match.")

        # Find a suitable opponent for player1
        potential_opponents = AvailablePlayer.objects.filter(is_available=True).exclude(player=player1).order_by('elo')

        if potential_opponents.exists():
            player2 = potential_opponents.first().player
            available_player1.is_available = False
            available_player1.save()
            available_player2 = AvailablePlayer.objects.get(player=player2)
            available_player2.is_available = False
            available_player2.save()
            serializer.save(player1=player1, player2=player2)
        else:
            raise serializers.ValidationError("No suitable opponents found.")

class MatchResultView(generics.UpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        winner = User.objects.get(id=request.data.get('winner'))

        if winner not in [instance.player1, instance.player2]:
            return Response({"detail": "Invalid winner."}, status=status.HTTP_400_BAD_REQUEST)

        instance.winner = winner
        instance.result_reported = True
        instance.save()

        # Update ELO ratings
        player1 = instance.player1
        player2 = instance.player2

        def update_elo(winner, loser):
            K = 32
            winner_elo = winner.profile.elo
            loser_elo = loser.profile.elo

            expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
            expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

            winner.profile.elo += K * (1 - expected_winner)
            loser.profile.elo += K * (0 - expected_loser)

            winner.profile.save()
            loser.profile.save()

        if winner == player1:
            update_elo(player1, player2)
        else:
            update_elo(player2, player1)

        return Response(status=status.HTTP_200_OK)
