from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bar(models.Model):
    nombre = models.CharField(max_length=128)
    latitud = models.DecimalField(max_digits=9,decimal_places=6)
    longitud = models.DecimalField(max_digits=9,decimal_places=6)

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
