# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 08:30
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('synenosis', '0008_auto_20160424_0115'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP VIEW IF EXISTS synenosis_account",
            reverse_sql="""CREATE OR REPLACE VIEW synenosis_account AS
(SELECT 'bank' as account_type, account_id, id, number, label, balance, currency, institution_id FROM synenosis_bankaccount)
UNION
(SELECT 'wallet' as account_type, account_id, id, number, label, balance, currency, institution_id FROM synenosis_walletaccount);""",
            state_operations=None,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account_id',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name=b'Account id'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='institution_id',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name=b'Institution id'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_uuid',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name=b'Transaction uuid'),
        ),
        migrations.AlterField(
            model_name='walletaccount',
            name='account_id',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name=b'Account id'),
        ),
        migrations.RunSQL(
            sql="""CREATE OR REPLACE VIEW synenosis_account AS
(SELECT 'bank' as account_type, account_id, id, number, label, balance, currency, institution_id FROM synenosis_bankaccount)
UNION
(SELECT 'wallet' as account_type, account_id, id, number, label, balance, currency, institution_id FROM synenosis_walletaccount);""",
            reverse_sql="DROP VIEW IF EXISTS synenosis_account",
            state_operations=None,
        ),
    ]
