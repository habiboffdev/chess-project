from django.contrib import admin
from .models import AvailablePlayer, Match, Tournament, TournamentParticipant, TournamentMatch, TournamentRound
# Register your models here.

class AvailablePlayerAdmin(admin.ModelAdmin):
    list_display = ['player', 'is_available', ]
    list_filter = ['is_available']
    search_fields = ['player__username']

class MatchAdmin(admin.ModelAdmin):
    list_display = ['player1', 'player2']
    list_filter = ['result_reported','winner']
    search_fields = ['player1__username', 'player2__username']
    
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'player', 'score']
    list_filter = ['tournament']
    search_fields = ['player__username']
class TournamentMatchAdmin(admin.ModelAdmin):
    list_display = ['round', 'player1', 'player2', 'winner', 'draw']
    list_filter = ['round']
    search_fields = ['player1__username', 'player2__username']
class TournamentRoundAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'round_number']
    list_filter = ['tournament']
    search_fields = ['tournament__name']

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentParticipant, TournamentParticipantAdmin)
admin.site.register(TournamentMatch, TournamentMatchAdmin)
admin.site.register(TournamentRound, TournamentRoundAdmin)
admin.site.register(AvailablePlayer, AvailablePlayerAdmin)
admin.site.register(Match, MatchAdmin)