from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Users.models import User
from .models import AvailablePlayer, Match, Tournament, TournamentParticipant, TournamentMatch, TournamentRound
from .serializers import AvailablePlayerSerializer, MatchSerializer, TournamentSerializer, TournamentParticipantSerializer, TournamentMatchSerializer, TournamentLeaderboardSerializer, TournamentMatchDetailSerializer
from Chess.constants import Constants
from django.db import models
from .pairing import create_next_round, update_elo
from rest_framework.views import APIView
class CancelAvailabilityView(generics.GenericAPIView):
    queryset = AvailablePlayer.objects.all()
    serializer_class = AvailablePlayerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            available_player = AvailablePlayer.objects.get(player=request.user)
            available_player.delete()
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
    """
    API view for creating a chess match.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Perform the creation of a chess match.

        Args:
            serializer (MatchSerializer): The serializer for the match.

        Returns:
            Response: The response containing the match data.

        Raises:
            serializers.ValidationError: If the player is not available or already in a match.
        """
        player1 = self.request.user
        print(player1)

        # Check if player1 is available
        try:
            available_player1 = AvailablePlayer.objects.get(player=player1, is_available=True)
        except AvailablePlayer.DoesNotExist:
            raise serializers.ValidationError("Player is not available for a match.")

        # Check if player1 is already in a match
        if self.queryset.filter(player1=player1, result_reported=False).exists():
            raise serializers.ValidationError("Player is already in a match.")

        # Find a suitable opponent for player1
        potential_opponents = AvailablePlayer.objects.filter(is_available=True).exclude(player=player1).order_by('player__rating')

        if potential_opponents.exists():
            player2 = potential_opponents.first().player
            available_player1.delete()
            available_player2 = AvailablePlayer.objects.get(player=player2)
            available_player2.delete()
            match = serializer.save(player1=player1, player2=player2)   
            match_data = {
                "match_id": match.id,
                "player1": {
                    "id": player1.id,
                    "username": player1.username,
                    "elo": player1.rating,
                    "country": player1.country,
                    "age": player1.age,
                },
                "player2": {
                    "id": player2.id,
                    "username": player2.username,
                    "elo": player2.rating,
                    "country": player2.country,
                    "age": player2.age,
                }
            }
            return Response(match_data, status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError("No suitable opponents found.")

class TournamentLeaderboardView(generics.ListAPIView):
    serializer_class = TournamentLeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return TournamentParticipant.objects.filter(tournament_id=tournament_id).order_by('-score')


class MatchResultView(generics.UpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        winner = User.objects.get(id=request.data.get('winner'))
        draw = request.data.get('draw', False)
        if winner not in [instance.player1, instance.player2] and draw == False:
            return Response({"detail": "Invalid winner."}, status=status.HTTP_400_BAD_REQUEST)

        instance.winner = winner
        instance.result_reported = True
        instance.draw = draw
        instance.save()

        # Update ELO ratings
        player1 = instance.player1
        player2 = instance.player2


        if draw == True:
            update_elo(player1, player2, "draw")
        elif winner == player1:
            update_elo(player1, player2, "player1")
        else:
            update_elo(player2, player1, "player2")

        return Response(status=status.HTTP_200_OK)

class TournamentCreateView(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    

class TournamentListView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class TournamentParticipantCreateView(generics.CreateAPIView):
    queryset = TournamentParticipant.objects.all()
    serializer_class = TournamentParticipantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tournament_id = self.kwargs['tournament_id']
        player = self.request.user
        tournament = Tournament.objects.get(id=tournament_id)
        serializer.save(tournament=tournament, player=player)

class TournamentParticipantListView(generics.ListAPIView):
    serializer_class = TournamentParticipantSerializer

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return TournamentParticipant.objects.filter(tournament_id=tournament_id)


class TournamentMatchResultView(generics.UpdateAPIView):
    queryset = TournamentMatch.objects.all()
    serializer_class = TournamentMatchSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        winner_id = request.data.get('winner')
        draw = request.data.get('draw', False)

        if draw:
            instance.draw = True
            instance.save()
            TournamentParticipant.objects.filter(tournament=instance.round.tournament, player=instance.player1).update(score=models.F('score') + Constants.SCORE_ADD_FOR_DRAW_TOURNAMENT)
            TournamentParticipant.objects.filter(tournament=instance.round.tournament, player=instance.player2).update(score=models.F('score') + Constants.SCORE_ADD_FOR_DRAW_TOURNAMENT)
        else:
            winner = User.objects.get(id=winner_id)
            if winner not in [instance.player1, instance.player2]:
                return Response({"detail": "Invalid winner."}, status=status.HTTP_400_BAD_REQUEST)
            instance.winner = winner
            instance.save()

            TournamentParticipant.objects.filter(tournament=instance.round.tournament, player=winner).update(score=models.F('score') + Constants.SCORE_ADD_FOR_WIN_TOURNAMENT)
        if draw == True:
            update_elo(instance.player1, instance.player2, "draw")
        if winner == instance.player1:
            update_elo(instance.player1, instance.player2, "player1")
        if winner == instance.player2:
            update_elo(instance.player1, instance.player2, "player2")
        return Response(status=status.HTTP_200_OK)
class CreateNextRoundView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, tournament_id):
        try:
            # check that tournaments is started
            if not Tournament.objects.get(id=tournament_id).is_active:
                return Response({"detail": "Tournament is not active."}, status=status.HTTP_400_BAD_REQUEST)
            tournament = Tournament.objects.get(id=tournament_id)
            new_round = create_next_round(tournament)
            return Response({"detail": f"Round {new_round.round_number} created successfully."}, status=status.HTTP_201_CREATED)
        except Tournament.DoesNotExist:
            return Response({"detail": "Tournament not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UserCurrentMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_id):
        user = request.user
        current_round = TournamentRound.objects.filter(tournament_id=tournament_id).order_by('-round_number').first()

        if not current_round:
            return Response({"detail": "No current round found for this tournament."}, status=status.HTTP_404_NOT_FOUND)

        match = TournamentMatch.objects.filter(round=current_round, player1=user).first() or \
                TournamentMatch.objects.filter(round=current_round, player2=user).first()

        if not match:
            return Response({"detail": "No match found for the current round."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TournamentMatchDetailSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)