from django.shortcuts import render
from django.views.generic import ListView
from .models import Bar
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.geocoders import GoogleV3
# Create your views here.


# https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/
class BaresCercaDeDireccionList(ListView):
    model = Bar
    template_name = "listar_bares.html"
    def get_queryset(self):
        geocoder = GoogleV3()
        direccion, latlong = geocoder.geocode(self.kwargs['direccion_busqueda'])
        centro_de_busqueda_point = geos.Point(latlong[1], latlong[0])
        #distancia = {'m': 400}
        ## 0.0001 grados son aprox 10 metros
        distancia = 0.0001 * 40
        result = Bar.objects.filter(coordenadas__distance_lte=(centro_de_busqueda_point, distancia))

        for b in result:
            print(b)
        return result
