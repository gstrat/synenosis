from rest_framework import serializers
from .models import Institution, BankAccount, WalletAccount, Account, \
        Transaction
from rest_framework.exceptions import ValidationError


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='institution_id', read_only=True)

    class Meta:
        model = Institution
        fields = ('id', 'short_name', 'full_name', 'logo', 'website')


class AccountBaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='account_id', read_only=True)
    institution_id = serializers.SlugRelatedField(slug_field='institution_id',
            queryset=Institution.objects.all(), source='institution')


class BankAccountSerializer(AccountBaseSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'label', 'number', 'balance', 'currency',
                  'IBAN', 'type', 'swift_bic', 'institution_id')


class WalletAccountSerializer(AccountBaseSerializer):
    class Meta:
        model = WalletAccount
        fields = ('id', 'label', 'number', 'balance', 'currency',
                  'institution_id')


class AccountSerializer(AccountBaseSerializer):
    type = serializers.CharField(source='account_type')

    class Meta:
        model = Account
        fields = ('id', 'type', 'label', 'number', 'balance', 'currency',
                  'institution_id')


class AccountRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, BankAccount):
            serializer = BankAccountSerializer
        elif isinstance(value, WalletAccount):
            serializer = WalletAccountSerializer
        else:
            raise Exception('Invalid account')

        return serializer(value).data


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(source='transaction_uuid', read_only=True)
    id = serializers.CharField(source='transaction_id', required=False)

    class Meta:
        model = Transaction
        fields = ('uuid', 'id', 'this_account', 'other_account', 'status',
                  'type', 'description', 'posted', 'completed',
                  'balance_amount', 'balance_currency',
                  'value_amount', 'value_currency')

    def validate(self, data):
        """ Handle the account fields """
        def _validate_account(name):
            account_id = data.get(name)
            if account_id is None:
                return

            try:
                account = Account.objects.get(account_id=account_id)
            except Account.DoesNotExist:
                raise ValidationError({name: ['Account does not exist']})
            else:
                data['%s_type' % name] = account.account_type

        _validate_account('this_account')
        _validate_account('other_account')

        return data
