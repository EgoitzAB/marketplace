# Generated by Django 5.0.4 on 2024-05-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_productoitem_talla_alter_categoria_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoitem',
            name='talla',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
