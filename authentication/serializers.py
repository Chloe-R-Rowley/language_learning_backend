# authentication/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username', '')
        email = validated_data.get('email', '')

        if not username:
            raise serializers.ValidationError("Username is required for registration.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with that username already exists.")

        if not email:
            raise serializers.ValidationError("Email is required for registration.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")

        user = User.objects.create_user(**validated_data)

        # Return the user details in the response
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context['request'].user

        # Adding user details to the response
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': getattr(user, 'first_name', '')
        }
        return data
