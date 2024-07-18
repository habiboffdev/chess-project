# in serializers.py
from rest_framework import serializers
from .models import User

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


