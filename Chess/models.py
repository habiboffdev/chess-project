from django.db import models

# Create your models here.

from Users.models import User

class AvailablePlayer(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_available = models.BooleanField(default=True)
    elo = models.IntegerField(default=1200)

class Match(models.Model):
    player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.SET_NULL, null=True, blank=True)
    match_date = models.DateTimeField(auto_now_add=True)
    result_reported = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player1.username} vs {self.player2.username}'
    
    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-match_date']
        
