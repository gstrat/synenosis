"""
WARNING: This is not a proper REST API consumer.
Due to time restrictions, we use a traditional HTTP workflow,
which is rapid in the django stack.
"""
from django.views.generic.base import TemplateView
from django.db.models.aggregates import Sum
from synenosis.models import BankAccount, WalletAccount, Account, \
        Transaction


class Dashboard(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['title'] = 'Dashboard'
        context['title_icon'] = 'home'

        context['accounts'] = {
            'winbank': BankAccount.objects \
                .filter(institution__short_name='PIRBGRAA').count(),
            'nbg': BankAccount.objects \
                .filter(institution__short_name='ETHNGRAA').count(),
            'paypal': WalletAccount.objects \
                .filter(institution__short_name='PAYPAL').count(),
            'all': Account.objects.all(),
            'total': Account.objects.aggregate(Sum('balance'))
        }

        transactions = list(Transaction.objects.order_by('-posted').all())
        for trans in transactions:
            for account in context['accounts']['all']:
                if account.account_id == trans.this_account and \
                        account.account_type == trans.this_account_type:
                    trans.account = account
                    break
        context['transactions'] = transactions

        return context