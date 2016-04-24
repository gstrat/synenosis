import datetime
from decimal import Decimal
from paypal.interface import PayPalInterface
from django.utils.timezone import now


class MyPayPalInterface(PayPalInterface):
    def get_balance(self, **kwargs):
        return self._call('GetBalance', **kwargs)

    def get_pal_details(self, **kwargs):
        return self._call('GetPalDetails', **kwargs)


class PayPalConnector(object):
    def __init__(self, username, password, signature):
        self.username = username
        self.password = password
        self.signature = signature

    def _get_interface(self):
        return MyPayPalInterface(
            API_USERNAME=self.username,
            API_PASSWORD=self.password,
            API_SIGNATURE=self.signature,
            API_ENVIRONMENT='PRODUCTION'
        )

    def get_account(self):
        pi = self._get_interface()
        account_details = pi.get_pal_details()
        balance_details = pi.get_balance()

        return {
            'number': account_details['PAL'],
            'balance': balance_details['L_AMT0'],
            'currency': balance_details['L_CURRENCYCODE0']
        }

    def get_transactions(self, start_date=None):
        start_date = start_date or (now() - datetime.timedelta(days=5))
        pi = self._get_interface()
        transactions = []
        for item in pi.transaction_search(STARTDATE=start_date).items():
            if item['STATUS'] == 'Completed':
                transactions.append({
                    'transaction_id': item['TRANSACTIONID'],
                    'type': item['TYPE'],
                    'value_amount': Decimal(item['AMT']),
                    'value_currency': item['CURRENCYCODE'],
                    'status': 'COMPLETED',
                    'this_account_type': 'wallet',
                    'description': item['NAME'],
                    'posted': datetime.datetime \
                            .strptime(item['TIMESTAMP'],
                                      '%Y-%m-%dT%H:%M:%SZ')
                })
        return transactions
