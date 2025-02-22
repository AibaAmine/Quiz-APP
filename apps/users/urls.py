from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import LogoutAPIView, RegisterAPIView, LoginAPIView, UserProfileView,FollowCreateAPIView,UnfollowAPIView,FollowersListAPIView,FollowingListAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('auth/logout/',LogoutAPIView.as_view(),name = 'logout'),
    path('unfollow/<int:following_id>/',UnfollowAPIView.as_view(),name='unfollow_user'),
    path('follow/',FollowCreateAPIView.as_view(),name = 'follow_user'),
    path('followers/',FollowersListAPIView.as_view(),name = "followers_list"),
    path('followings/',FollowingListAPIView.as_view(),name = 'followings_list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
