import django_filters
from .models import ProductoItem


class FiltroProducto(django_filters.FilterSet):
    categoria = django_filters.CharFilter(field_name='producto__categoria__nombre', lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(method='filter_precio_min')
    precio_max = django_filters.NumberFilter(method='filter_precio_max')

    class Meta:
        model = ProductoItem
        fields = ['categoria', 'precio_min', 'precio_max']

    def filter_precio_min(self, queryset, name, value):
        return queryset.filter(precio__gte=value)

    def filter_precio_max(self, queryset, name, value):
        return queryset.filter(precio__lte=value)
