# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MutualFund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fund_name', models.CharField(max_length=50)),
                ('scheme_name', models.CharField(max_length=50)),
                ('purchase_date', models.DateField(default=django.utils.timezone.now)),
                ('invested_value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('current_value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('nominee', models.CharField(max_length=30)),
                ('customer', models.ForeignKey(related_name='mutualfunds', to='portfolio.Customer')),
            ],
        ),
    ]
