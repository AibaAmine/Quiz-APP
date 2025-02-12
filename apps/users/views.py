from rest_framework import views
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from apps.users.sirializers import UserRegisterSerializer,UserLoginSerializer,UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from django.contrib.auth import logout
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
            access_token = AccessToken.for_user(user)  # Generate access token 
            return Response({
                
                'access': str(access_token),
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