from django.urls import path
from .views import Home, RegisterUser, ManageUser, ChangePasswordView, UserInfoView, UserListView, UserLeaderboardView, GetUserInfoView


urlpatterns = [
    
    path('api/register/', RegisterUser.as_view(), name='register'),
    path('api/user/<int:user_id>/', ManageUser.as_view(), name='manage_user'),
    path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/user_info/', UserInfoView.as_view(), name='user_info'),
    path('api/users/', UserListView.as_view(), name='user_list'),
    path('api/leaderboard/', UserLeaderboardView.as_view(), name='user_leaderboard'),
    path('api/get_user/<user_id>/', GetUserInfoView.as_view(), name='get_user'),
]