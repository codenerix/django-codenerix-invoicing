# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-15 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0047_auto_20170907_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashdiary',
            name='closed_amount',
        ),
        migrations.RemoveField(
            model_name='cashdiary',
            name='opened_amount',
        ),
        migrations.AddField(
            model_name='cashdiary',
            name='closed_cards',
            field=models.FloatField(blank=True, null=True, verbose_name='Closed Cards'),
        ),
        migrations.AddField(
            model_name='cashdiary',
            name='closed_cash',
            field=models.FloatField(blank=True, null=True, verbose_name='Closed Cash'),
        ),
        migrations.AddField(
            model_name='cashdiary',
            name='opened_cards',
            field=models.FloatField(default=0, verbose_name='Opened Cards'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashdiary',
            name='opened_cash',
            field=models.FloatField(default=0, verbose_name='Opened Cash'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cashmovement',
            name='kind',
            field=models.CharField(choices=[('AMA', 'Amazon'), ('TRA', 'Wire transfer'), ('CAR', 'Card'), ('CAS', 'Cash'), ('CRE', 'Credit'), ('PYP', 'Paypal'), ('30C', '30 day credit'), ('60C', '60 day credit'), ('90C', '90 day credit')], max_length=3, verbose_name='Kind'),
        ),
        migrations.AlterField(
            model_name='cashmovement',
            name='kind_card',
            field=models.CharField(blank=True, choices=[('VIS', 'Visa'), ('MAS', 'MasterCard'), ('AME', 'American Express'), ('OTH', 'Other')], max_length=3, null=True, verbose_name='Kind Card'),
        ),
    ]
