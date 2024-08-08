from django.urls import path, re_path
from .views import (
    CustomProviderAuthView,
    CustomLogoutView, 
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView
)
urlpatterns = [
    re_path(r'^o/(?P<provider>\S+)/', CustomProviderAuthView.as_view(), name="provider-auth"),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', CustomLogoutView.as_view()),
]
