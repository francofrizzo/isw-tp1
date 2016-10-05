from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from .models import Bar, Calificacion, Caracteristica
from .forms import BarModelForm, CalificacionModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.geocoders import GoogleV3
from json_views.views import JSONListView
from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
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
        caracs = Caracteristica.objects.all()
        bares = result.all()
        for bar in result:
            califs = Calificacion.objects.filter(bar=bar)
            promedios = {}
            for c in caracs:
                promedios[c.nombre] = sum(calif.puntaje for calif in califs.filter(caracteristica=c))
                n = len(califs.filter(caracteristica=c))
                if n != 0:
                    promedios[c.nombre] /= float(n)
            for k, v in self.request.GET.items():
                try:
                    c = caracs.get(nombre=k)
                except ObjectDoesNotExist:
                    continue
                if promedios.get(k, False) and promedios[k] < int(v):
                    print("Excluyendo bar {}".format(bar.nombre))
                    bares = bares.exclude(id=bar.id)
                    break
        return bares

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
def calificar_bar(request, barid):
    user = request.user
    estebar = get_object_or_404(Bar, pk=barid)
    califs_estebar = Calificacion.objects.filter(bar=estebar, user=user)
    cant_caracteristicas = len(Caracteristica.objects.all())
    cant_caracteristicas_no_calificadas = cant_caracteristicas - len(Calificacion.objects.filter(bar=estebar, user=user))

    CalificacionModelFormSet = modelformset_factory(Calificacion, form=CalificacionModelForm, extra=cant_caracteristicas_no_calificadas )
    if request.method == "POST":
        fset = CalificacionModelFormSet(
            request.POST, request.FILES,
            queryset=califs_estebar,
        )
        if fset.is_valid():
            for form in fset:
                resdir = form.clean()
                try:
                    cal = Calificacion.objects.get(bar=estebar, user=request.user, caracteristica=resdir['caracteristica'])
                    cal.puntaje = resdir['puntaje']
                except:
                    cal = Calificacion(bar=estebar, user=request.user, caracteristica=resdir['caracteristica'], puntaje=resdir['puntaje'])
                cal.save()
    else:
        fset = CalificacionModelFormSet(queryset=califs_estebar)
    return render(request, "calificar.html", {"formset": fset, "bar": estebar})
