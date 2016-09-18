from django.conf.urls import url
from .views import BaresCercaDeDireccionList


urlpatterns = [
    url(r'(?P<direccion_busqueda>[^/]+)/(?P<distancia_metros>[\d]+)/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion'),
]