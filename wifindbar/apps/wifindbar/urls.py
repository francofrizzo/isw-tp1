from django.conf.urls import url
from .views import BaresCercaDeDireccionList, BarDetailView, BarCreateView,  BaresCercaDeCoordenadaJSONList, HomeView, calificar_bar


urlpatterns = [
    url(r'^nuevo/$', BarCreateView.as_view(success_url="/"), name="bar_create_view"),
    url(r'^bares_json/$', BaresCercaDeCoordenadaJSONList.as_view(), name="bares_json"),
    url(r'^calificar/(?P<barid>[\d]+)/$', calificar_bar, name="calificar_bar"),
    url(r'^(?P<direccion_busqueda>[^/]+)/(?P<distancia_metros>[\d]+)/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion'),
    url(r'^busqueda/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion_form'),
    url(r'^(?P<pk>[\d]+)/$', BarDetailView.as_view(), name="bar_detail_view"),
    url(r'^$', HomeView.as_view(), name='index'),
]
