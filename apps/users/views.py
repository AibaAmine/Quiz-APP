from apps.users.models import Follower
from rest_framework import views
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from apps.users.sirializers import FollowerSerializer, UserRegisterSerializer,UserLoginSerializer,UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from django.contrib.auth import logout
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

# Create your views here.

User = get_user_model()


# register endpoint 
class RegisterAPIView(generics.CreateAPIView):
    model = User
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # Override JWT


# login endpoint
class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # Override JWT
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            access_token = AccessToken.for_user(user)# Generate access token
            refresh_token = RefreshToken.for_user(user)  # Generate refresh token
        
            return Response({
                
                'access': str(access_token),
                'refresh': str(refresh_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # Clears session data (for SessionAuthentication users)
        return Response({"message": "Logged out successfully"}, status=200)
    
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
    
#api view to prevent users for following
class FollowCreateAPIView(generics.CreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        follower = self.request.user
        following_id = self.request.data.get("following") # Get the user to be followed from the request data   #! to access data of the request :'self.request.data'
        print("following id : ",following_id)
        print("follower id : ",follower.id)
        if follower.id == int(following_id):
            raise serializers.ValidationError("You cannot follow yourself.")
        
        #check if he allready follow him
        followings = Follower.objects.filter(follower = follower,following_id = following_id)
        if followings.exists():
            raise serializers.ValidationError("You are already following this user.")
    
        serializer.save(follower=self.request.user) #follower=self.request.user  this ensure that only logged in user is the follower 
        

#api view to unfollow a user
class UnfollowAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self): #responsible for retrieving a specific object from the database.
        follower = self.request.user
        following_id = self.kwargs['following_id']  # get the user id that he want to unfollow from url
        try:
            return Follower.objects.get(follower = follower ,following_id = following_id)
        except Follower.DoesNotExist:
            raise NotFound("You are not following this user.") 
        
         
# api view to get the logged in user followers list       
class FollowersListAPIView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        followers_list = Follower.objects.filter(following = user)
        
        return followers_list
    

#api view to get the logged in user following list 
class FollowingListAPIView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print("user id :", user.id)
        following_list = Follower.objects.filter(follower = user)
        return following_list


#api view to check if the user follows another user  
class IsFollowingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        user = self.request.user
        is_following = Follower.objects.filter(follower = user,following = user_id).exists()
        return Response("is following = ",is_following)
    
    