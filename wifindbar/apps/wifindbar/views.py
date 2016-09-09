from django.shortcuts import render
from django.views.generic import ListView
from .models import Bar
from django.contrib import messages
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.geocoders import GoogleV3
# Create your views here.


# https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/
class BaresCercaDeDireccionList(ListView):
    model = Bar
    template_name = "listar_bares.html"
    def get_queryset(self):
        ## 0.00001 grados son aprox 1.1 metros
        radio_en_metros = 400
        radio_en_grados_aproximado = 0.00001 * (radio_en_metros/1.1)
        geocoder = GoogleV3()
        location_centro_de_busqueda = geocoder.geocode(self.kwargs['direccion_busqueda'])
        if location_centro_de_busqueda:
            point_centro_de_busqueda = geos.Point(y=location_centro_de_busqueda.latitude, x=location_centro_de_busqueda.longitude, srid=4326)
            result = Bar.objects.filter(coordenadas__distance_lte=(point_centro_de_busqueda, distancia))
        else:
            messages.warning(request, "No pudimos obtener la ubicación de la dirección ingresada.")
            return Bar.objects.none()
        return result
