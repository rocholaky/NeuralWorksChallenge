from django.db import models
from django.utils.timezone import now


# Create your models here.
class Consultas(models.Model):
    OPERA = models.CharField(max_length=100, null=False)
    TIPOVUELO = models.CharField(max_length=100, null=False)
    MES = models.CharField(max_length=100, null=False)
    VLO_I = models.CharField(max_length=5, null=False)
    fecha_consulta = models.DateField(default=now)
    PREDICCION = models.BooleanField(null=False)