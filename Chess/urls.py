from django.urls import path
from .views import (SetAvailablePlayerView, MatchCreateView, MatchResultView, CancelAvailabilityView, CreateNextRoundView, TournamentMatchResultView, 
                    TournamentCreateView, TournamentListView, TournamentDetailView, TournamentParticipantListView, TournamentParticipantCreateView, TournamentLeaderboardView, UserCurrentMatchView)

urlpatterns = [
    path('players/available/', SetAvailablePlayerView.as_view(), name='create_available_player'),
    path('matches/', MatchCreateView.as_view(), name='create_match'),
    path('matches/<int:pk>/result/', MatchResultView.as_view(), name='report_match_result'),
    path('players/available/cancel/', CancelAvailabilityView.as_view(), name='cancel_available_player'),
    path('tournaments/<int:tournament_id>/rounds/', CreateNextRoundView.as_view(), name='create_next_round'),
    path('tournaments/matches/<int:pk>/result/', TournamentMatchResultView.as_view(), name='report_match_result'),
    path('tournaments/', TournamentCreateView.as_view(), name='create_tournament'),
    path('tournaments/list/', TournamentListView.as_view(), name='list_tournaments'),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournaments/<int:tournament_id>/participants/', TournamentParticipantListView.as_view(), name='list_tournament_participants'),
    path('tournaments/<int:tournament_id>/participants/join/', TournamentParticipantCreateView.as_view(), name='join_tournament'),
    path('tournaments/<int:tournament_id>/leaderboard/', TournamentLeaderboardView.as_view(), name='tournament_leaderboard'),   
    path('tournaments/<int:tournament_id>/current_match/', UserCurrentMatchView.as_view(), name='user_current_match'),
]
