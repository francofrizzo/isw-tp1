# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 21:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifindbar', '0004_auto_20160909_0644'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calificacion',
            options={'verbose_name': 'calificación', 'verbose_name_plural': 'calificaciones'},
        ),
        migrations.AlterModelOptions(
            name='caracteristica',
            options={'verbose_name': 'característica', 'verbose_name_plural': 'características'},
        ),
        migrations.AlterField(
            model_name='calificacion',
            name='puntaje',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
