from django.urls import path
from .views import PondAPIView

urlpatterns = [
    path('ponds/', PondAPIView.as_view(), name='data_ponds'),
]
