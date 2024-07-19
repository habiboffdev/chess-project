import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Users.models import User
from Chess.models import Tournament, TournamentParticipant, TournamentRound, TournamentMatch

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username, password, is_staff=False):
        return User.objects.create_user(username=username, password=password, is_staff=is_staff)
    return _create_user

@pytest.fixture
def create_tournament():
    def _create_tournament(name):
        try:
            if Tournament.objects.get(name=name):
                return Tournament.objects.get(name=name)
        except:
            return Tournament.objects.create(name=name, start_date='2021-01-01', end_date='2021-01-02', is_active = True)
    return _create_tournament

@pytest.fixture
def create_tournament_participant(create_tournament, create_user):
    def _create_tournament_participant(tournament_name, username, password, is_staff=True):
        tournament = create_tournament(tournament_name)
        user = create_user(username, password, is_staff)
        return TournamentParticipant.objects.create(tournament=tournament, player=user)
    return _create_tournament_participant
@pytest.mark.django_db
def test_create_tournament_round(api_client, create_tournament_participant):
    participant1 = create_tournament_participant('Tournament 1', 'user1', 'testpass123')
    participant2 = create_tournament_participant('Tournament 1', 'user2', 'testpass123')

    url = reverse('create_next_round', args=[participant1.tournament.id])
    api_client.force_authenticate(user=participant1.player)
    response = api_client.post(url)
    assert response.status_code == 201
    assert TournamentRound.objects.filter(tournament=participant1.tournament).exists()
    assert TournamentMatch.objects.filter(round__tournament=participant1.tournament).count() == 1
@pytest.mark.django_db
def test_report_match_result(api_client, create_tournament_participant):
    participant1 = create_tournament_participant('Tournament 2', 'user1', 'testpass123')
    participant2 = create_tournament_participant('Tournament 2', 'user2', 'testpass123')

    round_url = reverse('create_next_round', args=[participant1.tournament.id])
    api_client.force_authenticate(user=participant1.player)
    api_client.post(round_url)

    match = TournamentMatch.objects.filter(round__tournament=participant1.tournament).first()
    result_url = reverse('report_match_result', args=[match.id])
    response = api_client.patch(result_url, {'winner': participant1.player.id})
    assert response.status_code == 200
    match.refresh_from_db()
    assert match.winner == participant1.player
@pytest.mark.django_db
def test_get_tournament_leaderboard(api_client, create_tournament_participant):
    participant1 = create_tournament_participant('Tournament 3', 'user1', 'testpass123')
    participant2 = create_tournament_participant('Tournament 3', 'user2', 'testpass123')

    leaderboard_url = reverse('tournament_leaderboard', args=[participant1.tournament.id])
    api_client.force_authenticate(user=participant1.player)
    response = api_client.get(leaderboard_url)
    assert response.status_code == 200
    assert len(response.data) == 2
@pytest.mark.django_db
def test_get_user_current_match(api_client, create_tournament_participant):
    participant1 = create_tournament_participant('Tournament 4', 'user1', 'testpass123')
    participant2 = create_tournament_participant('Tournament 4', 'user2', 'testpass123')

    round_url = reverse('create_next_round', args=[participant1.tournament.id])
    api_client.force_authenticate(user=participant1.player)
    api_client.post(round_url)

    match_url = reverse('user_current_match', args=[participant1.tournament.id])
    response = api_client.get(match_url)
    assert response.status_code == 200
    assert response.data['player1'] == 'user1' or response.data['player2'] == 'user1'
@pytest.mark.django_db
def test_scoring_after_win(api_client, create_tournament_participant):
    participant1 = create_tournament_participant('Tournament 1', 'user1', 'testpass123')
    participant2 = create_tournament_participant('Tournament 1', 'user2', 'testpass123')
    participant3 = create_tournament_participant('Tournament 1', 'user3', 'testpass123')
    round_url = reverse('create_next_round', args=[participant1.tournament.id])
    api_client.force_authenticate(user=participant1.player)
    api_client.post(round_url)
    
    match = TournamentMatch.objects.filter(round__tournament=participant1.tournament).first()
    result_url = reverse('report_match_result', args=[match.id])
    response = api_client.patch(result_url, {'winner': participant1.player.id})
    
    assert response.status_code == 200
    assert TournamentParticipant.objects.get(player=participant1.player).score == 2
    assert TournamentParticipant.objects.get(player=participant2.player).score == 0
    assert TournamentParticipant.objects.get(player=participant3.player).score == 1