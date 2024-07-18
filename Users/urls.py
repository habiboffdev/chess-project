from django.urls import path
from .views import Home, register_user, manage_user


urlpatterns = [
    path('', Home.as_view()),
    path('api/register/', register_user, name='register_user'),
    path('api/user/<int:user_id>/', manage_user, name='manage_user'),
]