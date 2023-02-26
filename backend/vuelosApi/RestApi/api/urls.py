from django.urls import path
from vuelosApi.RestApi.api.views import  AtrasosApi

app_name = 'atrasos'

urlpatterns = [
    path('estaAtrasado', AtrasosApi.as_view(), name='prediccion vuelo atrasado'),
]