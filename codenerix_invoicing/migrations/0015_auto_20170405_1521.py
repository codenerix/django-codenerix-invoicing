# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0014_auto_20170405_1344'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='wishlistproduct',
            name='product_final',
        ),
        migrations.RemoveField(
            model_name='wishlistproduct',
            name='wish_list',
        ),
        migrations.AddField(
            model_name='salesbasket',
            name='name',
            field=models.CharField(default='Mi cesta', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
        migrations.DeleteModel(
            name='WishListProduct',
        ),
    ]