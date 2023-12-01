from rest_framework import serializers
from ponds.models import Pond

class PondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pond
        fields = '__all__'
