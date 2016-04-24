import uuid
from decimal import Decimal
from django.db import models
from . import settings as ls

def get_uuid():
    return '%s' % uuid.uuid4()

class Institution(models.Model):
    institution_id = models.CharField(default=get_uuid,
            verbose_name='Institution id', max_length=255)
    short_name = models.CharField(max_length=32, verbose_name='Short name')
    full_name = models.CharField(max_length=255, verbose_name='Full name')
    logo = models.ImageField(blank=True, null=True, verbose_name='Logo')
    website = models.URLField(max_length=255, verbose_name='Website')

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    def __unicode__(self):
        return '%s' % self.institution_id


class AccountBase(models.Model):
    account_id = models.CharField(default=get_uuid, verbose_name='Account id',
                                   max_length=255)
    institution = models.ForeignKey(Institution, verbose_name='Institution')
    label = models.CharField(max_length=128, blank=True, verbose_name='Label')
    number = models.CharField(max_length=64, verbose_name='Number', unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2,
            default=Decimal('0.00'), verbose_name='Balance')
    currency = models.CharField(max_length=3, choices=ls.CURRENCIES,
            verbose_name='Currency')

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s' % self.account_id


class BankAccount(AccountBase):
    IBAN = models.CharField(max_length=128, verbose_name='IBAN', unique=True)
    type = models.CharField(max_length=128, verbose_name='Type')
    swift_bic = models.CharField(max_length=128, blank=True, 
            verbose_name='Swift code')

    class Meta:
        verbose_name = 'Bank account'
        verbose_name_plural = 'Bank accounts'


class WalletAccount(AccountBase):
    class Meta:
        verbose_name = 'Wallet account'
        verbose_name_plural = 'Wallet accounts'


class Account(AccountBase):
    account_type = models.CharField(max_length=6, choices=ls.ACCOUNT_TYPES,
            verbose_name='Account type')

    class Meta:
        managed = False
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def delete(self, using=None):
        raise NotImplemented

    def save(self, *args, **kwargs):
        raise NotImplemented


class Transaction(models.Model):
    transaction_uuid = models.CharField(default=get_uuid, max_length=255,
            verbose_name='Transaction uuid')
    transaction_id = models.CharField(max_length=64, blank=True,
            verbose_name='Transaction id',
            help_text='The bank\'s id for the transaction')
    this_account = models.CharField(verbose_name='This account', max_length=255)
    this_account_type = models.CharField(max_length=6, choices=ls.ACCOUNT_TYPES,
            verbose_name='This account type')
    other_account = models.CharField(null=True, blank=True, verbose_name='Other account',
                                     max_length=255)
    other_account_type = models.CharField(max_length=6, choices=ls.ACCOUNT_TYPES,
            verbose_name='Other account type', blank=True)
    status = models.CharField(max_length=9, choices=ls.STATUS_TYPES,
            verbose_name='Status', default='completed')
    type = models.CharField(max_length=128, verbose_name='Type')
    description = models.CharField(max_length=255, blank=True,
            verbose_name='Description')
    posted = models.DateTimeField(verbose_name='Posted datetime')
    completed = models.DateTimeField(null=True,
            verbose_name='Completed datetime')
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2,
            verbose_name='New balance amount', null=True, blank=True)
    balance_currency = models.CharField(max_length=3, choices=ls.CURRENCIES,
            verbose_name='New balance currency', blank=True)
    value_amount = models.DecimalField(max_digits=12, decimal_places=2,
            default=Decimal('0.00'), verbose_name='Value amount')
    value_currency = models.CharField(max_length=3, choices=ls.CURRENCIES,
            verbose_name='Value currency')
    comment = models.TextField(blank=True, verbose_name='Comment')

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __unicode__(self):
        return '%s' % self.transaction_uuid

