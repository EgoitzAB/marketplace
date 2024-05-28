from django.db import models

# Create your models here.
class Secciones(models.Model):
    """
    Model representing a section.

    Attributes:
        seccion (str): The name of the section.
        texto (str): The text content of the section.
        imagen (ImageField): The image associated with the section.
        created (DateTimeField): The date and time when the section was created.
        updated (DateTimeField): The date and time when the section was last updated.
    """

    seccion = models.CharField(max_length=50)
    indice = models.IntegerField(blank=True, null=True)
    texto = models.TextField()
    imagen = models.ImageField(upload_to='secciones', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now_add=True)
    categoria_choices = [
        ('nosotros', 'Nosotros'),
    ]
    categoria = models.CharField(max_length=10, choices=categoria_choices, default='nosotros')

    class Meta:
        ordering = ['indice']

    def __str__(self):
        return self.seccion
