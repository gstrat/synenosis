from rest_framework import viewsets
from .models import Institution, BankAccount, WalletAccount, Transaction
from .serializers import InstitutionSerializer, BankAccountSerializer, \
        WalletAccountSerializer, Account, AccountSerializer, TransactionSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()
    lookup_field = 'institution_id'
    http_method_names = ['get', 'post', 'head', 'delete']


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'account_id'
    http_method_names = ['get', 'post', 'head', 'delete']


class BankAccountViewSet(AccountViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()


class WalletViewSet(AccountViewSet):
    serializer_class = WalletAccountSerializer
    queryset = WalletAccount.objects.all()


class AccountListing(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    http_method_names = ['get']


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'transaction_uuid'
    http_method_names = ['get', 'post', 'head', 'delete']
