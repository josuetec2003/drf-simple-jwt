from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.state import token_backend



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Username or Password does not matched.'
    }
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        claims = [perm.code for perm in user.permission.all()]

        token['full_name'] = user.get_full_name() or 'SysAdmin'
        token['claims'] = claims
        token['is_admin'] = True

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ------

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        #data.update({'custom_field': 'custom_data'})        
        return data

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
