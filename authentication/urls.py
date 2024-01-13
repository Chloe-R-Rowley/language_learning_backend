from django.urls import path
from .views import UserLoginView, UserLogoutView, TokenRefreshView, CustomTokenObtainPairView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('custom-login/', CustomTokenObtainPairView.as_view(), name='custom-user-login'),
]