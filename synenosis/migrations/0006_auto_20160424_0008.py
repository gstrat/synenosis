# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 00:08
from __future__ import unicode_literals

from django.db import migrations

def init_data(apps, schema_editor):
    Institution = apps.get_model('synenosis', 'institution')
    Institution.objects.create(short_name='PIRBGRAA', full_name='Piraeus Bank',
                                website='http://www.piraeusbank.gr/')
    Institution.objects.create(short_name='ETHNGRAA', full_name='National Bank of Greece',
                                website='http://www.nbg.gr/')
    Institution.objects.create(short_name='PAYPAL', full_name='PayPal',
                                website='https://www.paypal.com/')

def delete_data(apps, schema_editor):
    Institution = apps.get_model('synenosis', 'institution')
    Institution.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('synenosis', '0005_transaction'),
    ]

    operations = [
            migrations.RunPython(init_data, reverse_code=delete_data)
    ]
