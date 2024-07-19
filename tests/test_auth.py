import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from Users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username, password, is_active=True):
        return User.objects.create_user(username=username, password=password, is_active=is_active)
    return _create_user

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(username='testuser').exists()
@pytest.mark.django_db
def test_token_obtain(api_client, create_user):
    user = create_user('testuser', 'testpass123')
    url = reverse('token_obtain_pair')
    data = {
        'username': user.username,
        'password': 'testpass123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
@pytest.mark.django_db
def test_token_obtain_inactive_user(api_client, create_user):
    user = create_user('inactiveuser', 'testpass123', is_active=False)
    url = reverse('token_obtain_pair')
    data = {
        'username': user.username,
        'password': 'testpass123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 401
    assert 'No active account found' in str(response.data)
@pytest.mark.django_db
def test_token_refresh(api_client, create_user):
    user = create_user('testuser', 'testpass123')
    url_obtain = reverse('token_obtain_pair')
    url_refresh = reverse('token_refresh')
    data = {
        'username': user.username,
        'password': 'testpass123'
    }
    response_obtain = api_client.post(url_obtain, data)
    refresh_token = response_obtain.data['refresh']

    response_refresh = api_client.post(url_refresh, {'refresh': refresh_token})
    assert response_refresh.status_code == 200
    assert 'access' in response_refresh.data
@pytest.mark.django_db
def test_token_refresh_inactive_user(api_client, create_user):
    user = create_user('testuser', 'testpass123')
    url_obtain = reverse('token_obtain_pair')
    url_refresh = reverse('token_refresh')
    data = {
        'username': user.username,
        'password': 'testpass123'
    }
    response_obtain = api_client.post(url_obtain, data)
    refresh_token = response_obtain.data['refresh']

    user.is_active = False
    user.save()

    response_refresh = api_client.post(url_refresh, {'refresh': refresh_token})
    assert response_refresh.status_code == 400
    assert 'inactive' in str(response_refresh.data)
