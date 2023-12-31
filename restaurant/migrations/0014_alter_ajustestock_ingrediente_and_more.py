# Generated by Django 4.2.5 on 2023-11-29 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0013_alter_ajustestock_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajustestock',
            name='ingrediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.ingrediente'),
        ),
        migrations.AlterField(
            model_name='ajustestock',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pedidoproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.categoria'),
        ),
        migrations.AlterField(
            model_name='productoingrediente',
            name='ingrediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.ingrediente'),
        ),
    ]
