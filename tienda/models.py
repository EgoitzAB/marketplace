from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User


from PIL import Image
from io import BytesIO
import uuid


class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
        ]
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)

        if self.imagen:
            try:
                img = Image.open(self.imagen)
                img = img.resize((800, 600))
                # Convertir la imagen a formato JPEG
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # Sobrescribir la imagen original con la nueva imagen
                self.imagen = ContentFile(buffer.getvalue())
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tienda:producto_listado_por_categoria',
                    args=[self.slug])


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,
                            related_name='productos',
                            on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(editable=False)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d',
                            blank=True)
    descripcion = models.TextField(blank=True)
    disponibilidad = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['nombre']),
            models.Index(fields=['-creado']),
            models.Index(fields=['categoria'])
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tienda:detalle_producto',
                    args=[self.id, self.slug])

class ProductoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="precios")
    precio = models.PositiveSmallIntegerField()
    peso = models.PositiveSmallIntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField(blank=True, null=True)
    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.producto.nombre}-{self.peso}")

        if self.imagen:
            try:
                img = Image.open(self.imagen)
                img = img.resize((800, 600))
                # Convertir la imagen a formato JPEG
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # Sobrescribir la imagen original con la nueva imagen
                self.imagen = ContentFile(buffer.getvalue())
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        super().save(*args, **kwargs)

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')
        ordering = ['-agregado']

    def __str__(self):
        return f'{self.usuario} - {self.producto}'
