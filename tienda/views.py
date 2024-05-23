from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Producto, ProductoItem
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import FileResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control
from django.conf import settings
from carrito.forms import CarritoAñadirProductoForm
from .recomendador import Recomendador
from .filtro import FiltroProducto

# Create your views here.
class PrincipalView(View):
    def get(self, request):
        productos = Producto.objects.filter(disponibilidad=True).order_by('categoria')
        categorias_con_productos = {}
        for producto in productos:
            if producto.categoria not in categorias_con_productos:
                categorias_con_productos[producto.categoria] = []
            categorias_con_productos[producto.categoria].append(producto)
        context = {
            'categorias_con_productos': categorias_con_productos,
        }
        return render(request, 'tienda/index.html', context)


class CategoriasView(ListView):
    model = Producto
    template_name = 'tienda/listado.html'
    context_object_name = 'productos'

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_seleccionada = self.request.GET.get('categoria')
        if categoria_seleccionada:
            queryset = queryset.filter(categoria__nombre__icontains=categoria_seleccionada)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aplicar el filtro
        filtro = FiltroProducto(self.request.GET, queryset=ProductoItem.objects.all())
        context['filtro'] = filtro
        return context


class ProductoDetalleView(DetailView):
    model = Producto
    template_name = 'tienda/detalle.html'

    def get_object(self):
        return get_object_or_404(Producto, slug=self.kwargs['slug'], disponibilidad=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        formulario_carrito = CarritoAñadirProductoForm()
        r = Recomendador()
        productos_recomendados = r.recomendar_productos_para([producto], 4)
        context.update({
            'formulario_carrito': formulario_carrito,
            'productos_recomendados': productos_recomendados,
        })
        return context

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    file_path = settings.BASE_DIR / "static" / "favicon.ico"
    with open(file_path, "rb") as file:
        return FileResponse(file, content_type="image/x-icon")