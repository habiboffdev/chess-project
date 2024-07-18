# in serializers.py
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer 
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email','age','full_name','country']  # add more fields as needed

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['age','full_name','country','is_active','rating']  # add more fields as needed

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        if not self.user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        user = User.objects.get(id=refresh['user_id'])
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        return data