from django.urls import path
from .views import PrincipalView, CategoriasView, ProductoDetalleView, favicon

app_name = "tienda"

urlpatterns = [
    path('', PrincipalView.as_view(), name="home"),
    path('productos/', CategoriasView.as_view(), name='listado_producto'),
    path('productos/<slug:slug>/', ProductoDetalleView.as_view(), name='detalle_producto'),
    path('favicon.ico', favicon, name='favicon'),
]