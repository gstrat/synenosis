from django.contrib import admin
from .models import Institution, BankAccount, WalletAccount, Transaction


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    readonly_fields = ['institution_id']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    readonly_fields = ['account_id']


@admin.register(WalletAccount)
class WalletAccountAdmin(admin.ModelAdmin):
    readonly_fields = ['account_id']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
