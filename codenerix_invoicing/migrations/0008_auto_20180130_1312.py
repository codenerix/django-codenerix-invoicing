# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-30 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0007_auto_20180129_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesbasket',
            name='pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_sales', to='codenerix_pos.POS', verbose_name='Point of Sales'),
        ),
        migrations.AlterField(
            model_name='salesbasket',
            name='pos_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_sales', to='codenerix_pos.POSSlot', verbose_name='POS Slot'),
        ),
    ]