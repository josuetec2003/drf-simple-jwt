from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', MyTokenRefreshView.as_view(), name='token_refresh'),
]