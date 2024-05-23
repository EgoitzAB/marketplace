from django.urls import path
from . import views


app_name = 'ordenes'


urlpatterns = [
    path('crear/', views.crear_orden, name='crear_orden'),
    path('admin/orden/<int:order_id>/', views.admin_orden_detalle,
                                        name='admin_orden_detalle'),
    path('admin/orden/<int:order_id>/pdf/',
        views.admin_orden_pdf,
        name='admin_orden_pdf'),
]