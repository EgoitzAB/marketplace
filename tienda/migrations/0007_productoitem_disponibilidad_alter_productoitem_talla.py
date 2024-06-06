# Generated by Django 5.0.4 on 2024-05-30 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_alter_productoitem_talla'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoitem',
            name='disponibilidad',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='productoitem',
            name='talla',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]