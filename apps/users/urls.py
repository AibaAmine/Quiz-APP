from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import LogoutAPIView, RegisterAPIView, LoginAPIView, UserProfileView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/',LogoutAPIView.as_view(),name = 'logout'),
  #  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
