# Generated by Django 4.2.5 on 2023-11-13 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_ajustestock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ajustestock',
            name='producto',
        ),
        migrations.AddField(
            model_name='ajustestock',
            name='ingrediente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='restaurant.ingrediente'),
            preserve_default=False,
        ),
    ]