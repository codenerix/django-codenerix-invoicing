# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-18 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0048_auto_20170915_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashdiary',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='Checked'),
        ),
        migrations.AddField(
            model_name='cashdiary',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
    ]