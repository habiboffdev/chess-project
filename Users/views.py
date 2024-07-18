from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, UserChangeSerializer
from Users.models import User


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        # Validate the refresh token as usual
        data = super().validate(attrs)
        
        # Extract the user from the refresh token
        refresh = RefreshToken(attrs['refresh'])
        user = User.objects.get(id=refresh['user_id'])

        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        
        # Return the validated data (new access token)
        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # The original validate method returns a dictionary with the tokens if the user is authenticated
        data = super().validate(attrs)
        
        # Check if the user is active
        if not self.user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        
        # If the user is active, return the token data
        return data

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    print(request.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manage_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        serializer = UserChangeSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserChangeSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted'}, status=204)