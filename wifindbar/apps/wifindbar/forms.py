from django.forms import ModelForm
from .models import Bar
from django.contrib.gis.forms import OSMWidget


# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
class BarModelForm(ModelForm):
    class Meta:
        model = Bar
        fields = ['nombre', 'direccion', 'ciudad', 'coordenadas']
        widgets = {
            'coordenadas': OSMWidget(attrs={'map_width': 800, 'map_height': 500})
        }
