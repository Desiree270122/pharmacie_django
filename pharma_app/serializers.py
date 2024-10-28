
from rest_framework import serializers

from .models import *

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'
        depth = 1