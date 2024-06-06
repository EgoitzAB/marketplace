import django_filters
from .models import Producto, Categoria


class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria']

