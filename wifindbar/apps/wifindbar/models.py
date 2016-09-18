from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

## Lecturas recomendadas:
# https://alastaira.wordpress.com/2011/01/23/the-google-maps-bing-maps-spherical-mercator-projection/
# https://docs.djangoproject.com/en/1.10/ref/contrib/gis/model-api/#selecting-an-srid
# http://postgis.net/docs/manual-2.1/using_postgis_dbmanagement.html#PostGIS_GeographyVSGeometry
# https://en.wikipedia.org/wiki/Decimal_degrees
# http://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude


# Create your models here.

class Bar(models.Model):
    nombre = models.CharField(max_length=128)
    direccion = models.CharField(blank=True,max_length=100)
    ciudad = models.CharField(blank=True,max_length=50)

    coordenadas = models.PointField(geography=True, blank=True, null=True)
    def __str__(self):
        return self.nombre



class Caracteristica(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    obligatoria = models.BooleanField(default=False)
    class Meta:
        verbose_name = "característica"
        verbose_name_plural = "características"
    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    user = models.ForeignKey(User)
    bar = models.ForeignKey(Bar)
    caracteristica = models.ForeignKey(Caracteristica)
    puntaje = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        unique_together = (("user", "bar", "caracteristica"), )
        index_together = (("bar", "caracteristica"), )
        verbose_name = "calificación"
        verbose_name_plural = "calificaciones"
