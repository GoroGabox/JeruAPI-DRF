# Generated by Django 4.2.5 on 2023-11-12 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_pedidodiario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidodiario',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]