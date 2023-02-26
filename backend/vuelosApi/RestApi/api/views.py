from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from vuelosApi.RestApi.models import Consultas
import numpy as np
from rest_framework import generics
from django.shortcuts import render
from django.http import HttpResponse
import sklearn
import pandas as pd
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from vuelosApi.settings import ModeloPredictivoAtrasos
from .serializers import AtrasoSerializer
from datetime import datetime

@api_view(["POST",])
def api_atrasos_view(request):
    if request.method =="POST":
        try: 
            information_json = json.loads(request.body.decode())
            data_vuelo = pd.DataFrame.from_dict(information_json["vuelos"])
            try:
                prediccion = ModeloPredictivoAtrasos.predict(data_vuelo)
            except: 
                return Response(status=status.HTTP_400_BAD_REQUEST)
            

            prediccion = {"result": np.where(prediccion, "Atrasado", "A la hora").tolist()}
            return Response(status=status.HTTP_200_OK, content=json.dumps(prediccion))
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET",])
def api_atrasos_view(request):
    if request.method =="POST":
        try: 
            information_json = json.loads(request.body.decode())
            data_vuelo = pd.DataFrame.from_dict(information_json["vuelos"])
            try:
                prediccion = ModeloPredictivoAtrasos.predict(data_vuelo)
            except: 
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
            prediccion = {"result": np.where(prediccion, "Atrasado", "A la hora").tolist()}
            return Response(status=status.HTTP_200_OK, content=json.dumps(prediccion))
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AtrasosApi(generics.ListAPIView):
    Serializer_class = AtrasoSerializer
    Serializer_instance = AtrasoSerializer(many=True)

    def get_queryset(self):
        desde = self.request.GET.get('desde', False)
        hasta = self.request.GET.get('hasta', False)
        desde = datetime.strptime(desde,'%d-%m-%Y').date() if desde else desde 
        hasta = datetime.strptime(hasta, '%d-%m-%Y').date() if hasta else hasta
        
        if (desde and hasta):
            historial_atrasos = Consultas.objects.filter(fecha_consulta__range=((desde), (hasta))).order_by("-fecha_consulta")
        else: 
            historial_atrasos = Consultas.objects.all().order_by("-fecha_consulta")
        self.queryset = historial_atrasos
        return self.queryset
    @csrf_exempt
    def post(self, request):
        if request.method =="POST":
            #try: 
                information_json = json.loads(request.body.decode())
                data_vuelo = pd.DataFrame.from_dict(information_json["vuelos"])
                try:
                    prediccion = pd.DataFrame(ModeloPredictivoAtrasos.predict(data_vuelo), columns=["PREDICCION"])
                except: 
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                
                data_vuelo = data_vuelo.join(prediccion)
                data_vuelo_serialized = list(data_vuelo.to_dict("index").values())
                #created_data = self.Serializer_instance.create(data_vuelo_serialized)
                data = data_vuelo_serialized
                return Response(data, status=status.HTTP_200_OK)
            #except:
            #    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @csrf_exempt
    def get(self, request):
        try:
            queryset = list(self.get_queryset())
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serialized_data = self.Serializer_class(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
