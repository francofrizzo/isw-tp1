from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from .models import Bar, Calificacion, Caracteristica
from .forms import BarModelForm, CalificacionModelForm, CalificacionFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.geocoders import GoogleV3
from json_views.views import JSONListView
from django.shortcuts import render_to_response
# Create your views here.

class HomeView(TemplateView):
    template_name = 'barescerca.html'


# https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/
class BaresCercaDeDireccionList(ListView):
    model = Bar
    template_name = "listar_bares.html"
    def get_queryset(self):
        ## 0.00001 grados son aprox 1.1 metros
        radio_en_metros = self.kwargs['distancia_metros']
        radio_en_grados_aproximado = 0.00001 * (int(radio_en_metros)/1.1)
        self.geocoder = GoogleV3()
        self.location_centro_de_busqueda = self.geocoder.geocode(self.kwargs['direccion_busqueda'])
        if self.location_centro_de_busqueda:
            point_centro_de_busqueda = geos.Point(y=self.location_centro_de_busqueda.latitude, x=self.location_centro_de_busqueda.longitude, srid=4326)
            result = Bar.objects.filter(coordenadas__distance_lte=(point_centro_de_busqueda, radio_en_grados_aproximado))
        else:
            messages.warning(request, "No pudimos obtener la ubicación de la dirección ingresada.")
            return Bar.objects.none()
        return result
    def get_context_data(self, **kwargs):
        context = super(BaresCercaDeDireccionList, self).get_context_data(**kwargs)
        context['location_centro_de_busqueda'] = self.location_centro_de_busqueda
        return context


class BarDetailView(DetailView):
    model = Bar
    template_name = "detalles_bar.html"
    def get_context_data(self, **kwargs):
       context = super(BarDetailView, self).get_context_data(**kwargs)
       context['calificaciones'] = Calificacion.objects.filter(bar=context['object'])
       return context


class BarCreateView(CreateView):
    form_class = BarModelForm
    template_name = "crear_bar.html"

class CalificacionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Calificacion
    form_class = CalificacionModelForm
    template_name = "crear_calificacion.html"

    def form_valid(self, form):
        calificacion = form.save(commit=False)
        calificacion.user = self.request.user
        return super(CalificacionCreateView, self).form_valid(form)

class BaresCercaDeCoordenadaJSONList(JSONListView):
    model = Bar
    def get_queryset(self):
        ## 0.00001 grados son aprox 1.1 metros
        radio_en_metros = self.request.GET.get('radio_en_metros')
        radio_en_grados_aproximado = 0.00001 * (int(radio_en_metros)/1.1)
        lat = float(self.request.GET.get('lat'))
        lng = float(self.request.GET.get('lng'))
        self.point_centro_de_busqueda = geos.Point(y=lat, x=lng, srid=4326)
        result = Bar.objects.filter(coordenadas__distance_lte=(self.point_centro_de_busqueda, radio_en_grados_aproximado))
        return result

@login_required
def calificar_bar(request):
    deportes = Bar.objects.get(id=6)
    califs_deportes = Calificacion.objects.filter(bar=deportes)
    todas_las_caracteristicas = Caracteristica.objects.all()
    initial_caracteristicas = [{'caracteristica': i,} for i in todas_las_caracteristicas]
    fset = CalificacionFormSet(queryset=califs_deportes, initial=initial_caracteristicas)
    return render_to_response("calificar.html", {"formset": fset,})
