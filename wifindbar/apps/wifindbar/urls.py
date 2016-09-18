from django.conf.urls import url
from .views import BaresCercaDeDireccionList, BarDetailView


urlpatterns = [
    url(r'(?P<direccion_busqueda>[^/]+)/(?P<distancia_metros>[\d]+)/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion'),
    url(r'(?P<pk>[\d]+)/$', BarDetailView.as_view(), name="bar_detail_view"),
]
