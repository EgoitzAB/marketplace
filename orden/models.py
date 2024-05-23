from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                MaxValueValidator
from localflavor.es.models import ESPostalCodeField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.conf import settings
from tienda.models import Producto
#from coupons.models import Coupon


class Orden(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField('nombre', max_length=50)
    apellido = models.CharField('apellido', max_length=50)
    email = models.EmailField('e-mail')
    telefono = PhoneNumberField()
    direccion = models.CharField('dirección', max_length=250)
    codigo_postal = ESPostalCodeField()
    provincia = models.CharField(max_length=100)
    ciudad = models.CharField('ciudad', max_length=100)
    estado = models.CharField(max_length=100, default="España")
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    pagado = models.BooleanField(default=False)
#    stripe_id = models.CharField(max_length=250, blank=True)
#    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    descuento = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
                                    MaxValueValidator(100)])

    class Meta:
        ordering = ['-creado']
        indexes = [
            models.Index(fields=['-creado']),
        ]

    def __str__(self):
        return f'Orden {self.id}'

    def precio_antes_descuento(self):
        return sum(item.obtener_precio() for item in self.items.all())

    def obtener_descuento(self):
        precio_total = self.precio_antes_descuento()
        if self.descuento:
            return precio_total * (self.descuento / Decimal(100))
        return Decimal(0)

    def obtener_precio_total(self):
        precio_total = self.precio_antes_descuento()
        return precio_total - self.obtener_descuento()

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='orden_items', on_delete=models.CASCADE)
    sku = models.UUIDField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def obtener_precio(self):
        return self.precio * self.cantidad
