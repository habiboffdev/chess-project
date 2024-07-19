from django.contrib import admin
from .models import AvailablePlayer, Match
# Register your models here.

class AvailablePlayerAdmin(admin.ModelAdmin):
    list_display = ['player', 'is_available', 'elo']
    list_filter = ['is_available']
    search_fields = ['player__username']

class MatchAdmin(admin.ModelAdmin):
    list_display = ['player1', 'player2']
    list_filter = ['result_reported','winner']
    search_fields = ['player1__username', 'player2__username']
    
admin.site.register(AvailablePlayer, AvailablePlayerAdmin)
admin.site.register(Match, MatchAdmin)