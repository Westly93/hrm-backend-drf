from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Profile
class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response= super().post(request, *args, **kwargs)
        if response.status_code==201:
            access_token= response.data['access']
            refresh_token= response.data['refresh']
            response.set_cookie(
                'access',
                access_token,
                max_age= settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path= settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite= settings.AUTH_COOKIE_SAMESITE,
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age= settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path= settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite= settings.AUTH_COOKIE_SAMESITE,
            )
        return response 
            
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response= super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token= response.data['access']
            refresh_token= response.data['refresh']
            response.set_cookie(
                'access',
                access_token,
                max_age= settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path= settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite= settings.AUTH_COOKIE_SAMESITE,
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age= settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path= settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite= settings.AUTH_COOKIE_SAMESITE,
            )
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token= request.COOKIES.get('refresh')
        if refresh_token:
            request.data['refresh']= refresh_token
        response= super().post(request, *args, **kwargs)
        if response.status_code==200:
            access_token= response.data['access']
            response.set_cookie(
                'access',
                access_token,
                max_age= settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path= settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite= settings.AUTH_COOKIE_SAMESITE,
            )
        return response
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token= request.COOKIES.get('access')
        if access_token:
            request.data['token']= access_token
        return super().post(request, *args, **kwargs)
    
class CustomLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response= Response(status= status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    
class ProfileView(APIView):
    from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
    parser_classes= [FormParser, MultiPartParser, JSONParser]
    def get(self, request, *args, **kwargs):
        user= request.user
        profile= Profile.objects.get(user=user)
        serializer= ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user= request.user
        profile= Profile.objects.get(user=user)
        print(request.data)
        serializer= ProfileSerializer(instance= profile, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response({"message":"Ooops failed to update your profile something went wrong!!"})