from django.contrib.gis import admin
from .models import Bar, Caracteristica, Calificacion
# Register your models here.

admin.site.register(Bar, admin.OSMGeoAdmin)

admin.site.register(Caracteristica)
admin.site.register(Calificacion)
