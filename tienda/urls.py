from django.urls import path
from . import views

app_name = "tienda"

urlpatterns = [
    path('', views.PrincipalView.as_view(), name="home"),
    path('productos/', views.CategoriasView.as_view(), name='listado_producto'),
    path('productos/<slug:slug>/', views.ProductoDetalleView.as_view(), name='detalle_producto'),
    path('agregar-a-favoritos/<int:producto_id>/', views.AgregarFavoritoView.as_view(), name='agregar_a_favoritos'),
    path('eliminar-de-favoritos/<int:producto_id>/', views.EliminarFavoritoView.as_view(), name='eliminar_de_favoritos'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/favoritos/', views.favoritos, name='favoritos'),
    path('perfil/ordenes-no-finalizadas/', views.ordenes_no_finalizadas, name='ordenes_no_finalizadas'),
    path('perfil/historial-compras/', views.historial_compras, name='historial_compras'),
    path('favicon.ico', views.favicon, name='favicon'),
]