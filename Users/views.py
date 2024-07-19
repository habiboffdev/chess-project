from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer, UserChangeSerializer, ChangePasswordSerializer, UserInfoSerializer
from Users.models import User   

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # authentication_classes = []
    # permission_classes = [AllowAny]    

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    # authentication_classes = []
    # permission_classes = [AllowAny]
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        API view to register a new user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManageUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, user_id):
        """
        API view to get a user.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The ID of the user to get.

        Returns:
            Response: The HTTP response object.

        Raises:
            User.DoesNotExist: If the user with the specified ID does not exist.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        serializer = UserChangeSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        """
        API view to update a user.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The ID of the user to update.

        Returns:
            Response: The HTTP response object.

        Raises:
            User.DoesNotExist: If the user with the specified ID does not exist.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        serializer = UserChangeSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, user_id):
        """
        API view to delete a user.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The ID of the user to delete.

        Returns:
            Response: The HTTP response object.

        Raises:
            User.DoesNotExist: If the user with the specified ID does not exist.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        user.delete()
        return Response({'message': 'User deleted'}, status=204)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not check_password(current_password, user.password):
                return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all(sort_by='created_at')
        serializer = UserChangeSerializer(users, many=True)
        return Response(serializer.data)
    
class UserLeaderboardView(APIView):
    permission_classes = []

    def get(self, request):
        users = User.objects.all().order_by('-rating')
        serializer = UserChangeSerializer(users, many=True)
        return Response(serializer.data)
    
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if str(user_id).isdigit() == False:
            # return Response({'error': 'Invalid user ID'}, status=400)
            user = User.objects.get(username=user_id)
        else:
            user = User.objects.get(id=user_id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)
