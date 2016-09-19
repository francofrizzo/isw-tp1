from django.contrib import admin
from .models import Bar, Caracteristica, Calificacion
from .forms import BarModelForm
# Register your models here.

class BarAdmin(admin.ModelAdmin):
    form = BarModelForm

admin.site.register(Bar, BarAdmin)
admin.site.register(Caracteristica)
admin.site.register(Calificacion)
