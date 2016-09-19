import floppyforms.__future__ as forms
from .models import Bar, Caracteristica, Calificacion
from django.contrib.auth.models import User
from django.contrib.gis.forms import OSMWidget
from django.forms import inlineformset_factory

class PointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    google_maps_api_key = 'AIzaSyC7CRt0SLNHRJS0I9UkXupGNZiE1kEO2mM'

# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
class BarModelForm(forms.ModelForm):
    class Meta:
        model = Bar
        fields = ['nombre', 'direccion', 'ciudad', 'coordenadas']
        widgets = {
            'coordenadas': PointWidget()
        }

class CalificacionModelForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['bar', 'caracteristica', 'puntaje']

CalificacionFormSet = inlineformset_factory(Bar, Calificacion, fields=('puntaje', 'caracteristica', ))
