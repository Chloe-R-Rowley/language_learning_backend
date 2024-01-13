# authentication/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = serializer.data
        print("Response Data:", response_data)  
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshView(TokenRefreshView):
    pass

class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Log the refresh token for debugging
            print("Received refresh token:", refresh_token)

            # Attempt to blacklist the refresh token
            token = RefreshToken(refresh_token)
            print("Token is valid:", token.valid())

            if not token.valid():
                return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log any exceptions for debugging
            print("Exception:", str(e))
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)