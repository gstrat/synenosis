from django.views.generic import TemplateView
from demoapp.forms.accounts import AddWinbankAccountForm, AddNBGAccountForm, \
        AddPayPalAccountForm

"""
WARNING: This is not a proper REST API consumer.
Due to time restrictions, we use a traditional HTTP workflow,
which is rapid in the django stack.
"""

class AddWinbankAccount(TemplateView):
    template_name = 'accounts/add_winbank.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['title'] = 'Add Winbank account'
        context['title_icon'] = 'plus'
        context['form'] = AddWinbankAccountForm()
        return context


class AddNBGAccount(TemplateView):
    template_name = 'accounts/add_nbg.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['title'] = 'Add National Bank of Greece account'
        context['title_icon'] = 'plus'
        context['form'] = AddNBGAccountForm()
        return context


class AddPayPalAccount(TemplateView):
    template_name = 'accounts/add_paypal.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['title'] = 'Add PayPal account'
        context['title_icon'] = 'plus'
        context['form'] = AddPayPalAccountForm()
        return context
