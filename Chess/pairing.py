from .models import TournamentParticipant, TournamentMatch, TournamentRound
from django.db import models
from .constants import Constants
def swiss_pairings(tournament):
    participants = list(TournamentParticipant.objects.filter(tournament=tournament).order_by('-score'))
    pairs = []
    paired_players = set()

    while len(participants) > 1:
        player1 = participants.pop(0)
        found_opponent = False

        for idx, player2 in enumerate(participants):
            if not TournamentMatch.objects.filter(round__tournament=tournament, player1=player1.player, player2=player2.player).exists() and \
               not TournamentMatch.objects.filter(round__tournament=tournament, player1=player2.player, player2=player1.player).exists():
                pairs.append((player1.player, player2.player))
                paired_players.update({player1.player, player2.player})
                participants.pop(idx)
                found_opponent = True
                break

        if not found_opponent:
            participants.append(player1)  # Reinsert the player for the next round

    # If there's an odd player left without a match, they get a bye
    if participants:
        unpaired_player = participants.pop(0)
        pairs.append((unpaired_player.player, None))
        paired_players.add(unpaired_player.player)

    return pairs

def create_next_round(tournament):
    current_round_number = TournamentRound.objects.filter(tournament=tournament).count() + 1
    new_round = TournamentRound.objects.create(tournament=tournament, round_number=current_round_number)

    pairings = swiss_pairings(tournament)

    for player1, player2 in pairings:
        if player2:
            TournamentMatch.objects.create(round=new_round, player1=player1, player2=player2)
        else:
            # Bye round for unpaired player
            TournamentParticipant.objects.filter(tournament=tournament, player=player1).update(score=models.F('score') + Constants.BYE_POINTS)

    return new_round
def update_elo(player1, player2, result):
    K = Constants.K
    player1_elo = player1.rating
    player2_elo = player2.rating

    expected_player1 = 1 / (1 + 10 ** ((player2_elo - player1_elo) / 400))
    expected_player2 = 1 / (1 + 10 ** ((player1_elo - player2_elo) / 400))

    if result == "draw":
        player1.rating += K * (0.5 - expected_player1)
        player2.rating += K * (0.5 - expected_player2)
    elif result == "player1":
        player1.rating += K * (1 - expected_player1)
        player2.rating += K * (0 - expected_player2)
    elif result == "player2":
        player1.rating += K * (0 - expected_player1)
        player2.rating += K * (1 - expected_player2)

    player1.save()
    player2.save()