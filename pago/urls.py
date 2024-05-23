from django.urls import path
from django.conf import settings
from . import views

app_name = 'pago'

urlpatterns = [
    path('realizar-compra/', views.realizar_compra, name='create_order'),
    path('confirmacion/<int:compra_id>/', views.confirmacion_compra, name='confirmacion'),
    path('prueba-order/', views.prueba_order, name='prueba_order'),
    path('cancelacion/<int:compra_id>/', views.cancelacion_compra, name="cancelacion",)
]