from django.conf.urls import url
from .views import BaresCercaDeDireccionList


urlpatterns = [
    url(r'(?P<direccion_busqueda>[^/]+)/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion'),
]
