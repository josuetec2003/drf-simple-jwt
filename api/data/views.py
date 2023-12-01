from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from api.data.serializers import PondSerializer
from ponds.models import Pond

class PondAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    #throttle_classes = [UserRateThrottle]
    #permission_classes = [IsAuthenticated] 

    def get(self, request):
        print('GET Method executed')
        #import pdb; pdb.set_trace()
        # if request.user.is_anonymous:
        #     ponds = Pond.objects.all()
        #     serializer = PondSerializer(ponds, many=True)
        #     return Response(serializer.data)
        
        # Para cuando el usuario está autenticado (O sea que la url de esta vista está protegida con token)
        # permission_classes = [IsAuthenticated]
        permisos = [perm.code for perm in request.user.permission.all()]
        if 'pon' in permisos:
            ponds = Pond.objects.all()
            serializer = PondSerializer(ponds, many=True)
            return Response(serializer.data)
        
        import pdb; pdb.set_trace()

        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = PondSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

