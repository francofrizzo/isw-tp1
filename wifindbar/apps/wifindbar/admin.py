from django.contrib.gis import admin
from .models import Bar
# Register your models here.

admin.site.register(Bar, admin.OSMGeoAdmin)
