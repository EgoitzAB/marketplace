import django_filters
from .models import ProductoItem, Categoria

class FiltroProducto(django_filters.FilterSet):
    categoria = django_filters.ModelChoiceFilter(
        field_name='producto__categoria',
        queryset=Categoria.objects.all(),
        to_field_name='nombre',
        label='Categoría'
    )
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')

    class Meta:
        model = ProductoItem
        fields = ['categoria', 'precio_min', 'precio_max']
