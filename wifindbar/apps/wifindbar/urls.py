from django.conf.urls import url
from .views import BaresCercaDeDireccionList, BarDetailView, BarCreateView, CalificacionCreateView


urlpatterns = [
    url(r'nuevo/$', BarCreateView.as_view(success_url="/"), name="bar_create_view"),
    url(r'calificar/(?P<barid>[\d]+)/$', CalificacionCreateView.as_view(), name="calificacion_create_view"),
    url(r'(?P<pk>[\d]+)/$', BarDetailView.as_view(), name="bar_detail_view"),
    url(r'(?P<direccion_busqueda>[^/]+)/(?P<distancia_metros>[\d]+)/$', BaresCercaDeDireccionList.as_view(), name='listar_bares_cerca_de_direccion'),
]
