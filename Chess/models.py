from django.db import models

# Create your models here.

from Users.models import User
from .managers import  BaseLayer

class AvailablePlayer(BaseLayer):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

class Match(models.Model):
    player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.SET_NULL, null=True, blank=True)
    match_date = models.DateTimeField(auto_now_add=True)
    result_reported = models.BooleanField(default=False)
    draw = models.BooleanField(default=False)

    
    rating_change_winner = models.IntegerField(default=0)
    rating_change_loser = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.player1.username} vs {self.player2.username}'
    
    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-match_date']
        

class Tournament(BaseLayer):
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Tournaments'
        ordering = ['-start_date']
        
    def __str__(self):
        return self.name
class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
    player = models.OneToOneField(User, related_name='tournament_participations', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.player.username} in {self.tournament.name}'
    
class TournamentRound(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.IntegerField()

    def __str__(self):
        return f'{self.tournament.name} - Round {self.round_number}'

class TournamentMatch(models.Model):
    round = models.ForeignKey(TournamentRound, related_name='matches', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='tournament_matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='tournament_matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='tournament_wins', on_delete=models.SET_NULL, null=True, blank=True)
    draw = models.BooleanField(default=False)

    rating_change_winner = models.IntegerField(default=0)
    rating_change_loser = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.player1.username} vs {self.player2.username} - Round {self.round.round_number}'
2.