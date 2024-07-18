from django.urls import path
from .views import Home, RegisterUser, ManageUser, ChangePasswordView


urlpatterns = [
    path('', Home.as_view()),
    path('api/register/', RegisterUser.as_view(), name='register_user'),
    path('api/user/<int:user_id>/', ManageUser.as_view(), name='manage_user'),
    path('api/change_password/', ChangePasswordView.as_view(), name='change_password'),
    
]