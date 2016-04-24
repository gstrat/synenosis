from django import forms


class AddWinbankAccountForm(forms.Form):
    number = forms.CharField(label='Account number',
                             help_text='Internal Winbank account number')
    username = forms.CharField(label='Username',
                               help_text='Your Winbank web banking username')
    password = forms.CharField(label='Password',
                               help_text='Your Winbank web banking password',
                               widget=forms.PasswordInput)


class AddNBGAccountForm(forms.Form):
    account_id = forms.CharField(label='Account id',
                             help_text='Account id as found on the NBG API')
    key = forms.CharField(label='API key',
                               help_text='Your NBG REST api key',
                               widget=forms.PasswordInput)


class AddPayPalAccountForm(forms.Form):
    paypal_username = forms.CharField(label='Username',
                               help_text='Your PayPal API username')
    paypal_password = forms.CharField(label='Password',
                               help_text='Your PayPal API password',
                               widget=forms.PasswordInput)
    signature = forms.CharField(label='Signature',
                             help_text='Your PayPal API signature',
                             widget=forms.PasswordInput)

