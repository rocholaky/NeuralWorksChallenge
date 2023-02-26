from vuelosApi.RestApi.models import Consultas
from rest_framework import serializers
from rest_framework.decorators import api_view


class AtrasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields= "__all__"
