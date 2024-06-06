# tienda/admin.py
from django.contrib import admin
from .models import Categoria, Producto, ProductoItem

class ProductoItemInline(admin.TabularInline):
    model = ProductoItem
    extra = 1  # Number of extra forms to display

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ProductoItemInline]
    list_display = ('nombre', 'categoria', 'disponibilidad', 'creado', 'modificado')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('disponibilidad', 'categoria', 'creado', 'modificado')
    prepopulated_fields = {'slug': ('nombre',)}
    fields = ('nombre', 'slug', 'categoria', 'descripcion', 'disponibilidad', 'imagen')
    exclude = ('creado', 'modificado')

@admin.register(ProductoItem)
class ProductoItemAdmin(admin.ModelAdmin):
    list_display = ('producto', 'precio', 'peso', 'stock', 'sku')
    search_fields = ('producto__nombre', 'sku')
    list_filter = ('producto',)
