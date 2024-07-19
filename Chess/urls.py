from django.urls import path
from .views import SetAvailablePlayerView, MatchCreateView, MatchResultView

urlpatterns = [
    path('players/available/', SetAvailablePlayerView.as_view(), name='set_available_player'),
    path('matches/', MatchCreateView.as_view(), name='create_match'),
    path('matches/<int:pk>/result/', MatchResultView.as_view(), name='report_match_result'),
]
