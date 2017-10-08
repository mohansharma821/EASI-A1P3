# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('cust_number', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=200)),
                ('cell_phone', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('acquired_value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('acquired_date', models.DateField(default=django.utils.timezone.now)),
                ('recent_value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('recent_date', models.DateField(blank=True, null=True, default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(related_name='investments', to='portfolio.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('shares', models.DecimalField(max_digits=10, decimal_places=1)),
                ('purchase_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('purchase_date', models.DateField(blank=True, null=True, default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(related_name='stocks', to='portfolio.Customer')),
            ],
        ),
    ]
