from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bar(models.Model):
    nombre = models.CharField(max_length=128)
    # https://en.wikipedia.org/wiki/Decimal_degrees
    # http://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude
    latitud = models.DecimalField(max_digits=8,decimal_places=5)
    longitud = models.DecimalField(max_digits=8,decimal_places=5)

class Caracteristica(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    obligatoria = models.BooleanField(default=False)

class Calificacion(models.Model):
    user = models.ForeignKey(User)
    bar = models.ForeignKey(Bar)
    caracteristica = models.ForeignKey(Caracteristica)
    puntaje = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = (("user", "bar", "caracteristica"), )
        index_together = (("bar", "caracteristica"), )
