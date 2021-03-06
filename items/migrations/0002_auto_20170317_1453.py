# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-17 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuringinstrumenttype',
            name='checking_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personnel.Contractor', verbose_name='Проверяющая организация'),
        ),
        migrations.AddField(
            model_name='measuringinstrumenttype',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kinds', to='items.MeasuringInstrumentKind', verbose_name='Вид'),
        ),
        migrations.AddField(
            model_name='measuringinstrumenttype',
            name='suppliers',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='personnel.Contractor', verbose_name='Поставщики'),
        ),
        migrations.AddField(
            model_name='measuringinstrument',
            name='holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personnel.Job', verbose_name='Держатель'),
        ),
        migrations.AddField(
            model_name='measuringinstrument',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.MeasuringInstrumentType', verbose_name='Тип'),
        ),
    ]
