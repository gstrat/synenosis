# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from datetime import datetime
from bs4 import BeautifulSoup
from .base import SeleniumConnector
from selenium.webdriver.support.select import Select
from django.utils.timezone import utc


class WinbankConnector(SeleniumConnector):
    def login(self, username, password):
        self.driver.get("https://www.winbank.gr/el/Pages/Home.aspx")

        self.wait_for_id(element_id='_userAlias',
                         error_message='Could not connect')

        self.driver.find_element_by_id('_userAlias').send_keys(username)
        self.driver.find_element_by_id('_fakePassword').send_keys(password)
        self.driver.find_element_by_id('btnLogin').click()

        self.wait_for_id(element_id='_navigationControl__links1',
                         error_message='The credentials were not valid')

    def _go_to_portfolio(self):
        self.driver.find_element_by_id('_navigationActionLink_1_0').click()

        self.wait_for_id(element_id='_itemsTr',
                         error_message='The credentials were not valid')

    def _go_to_manage_accounts(self):
        self.driver.find_element_by_link_text(u'Διαχείριση Λογαριασμών').click()
        self.wait_for_link_text(link_text=u'Λογαριασμοί',
                                error_message='Could not connect')

    def _go_to_accounts(self):
        self.driver.find_element_by_link_text(u'Λογαριασμοί').click()
        self.wait_for_id(element_id='_mainContentPlaceHolder_accountsCtrl00__' \
                                    'accountDataList',
                         error_message='Could not connect')

    def _go_to_transactions(self, number):
        self.driver.find_element_by_link_text(u'Κινήσεις Λογαριασμών').click()
        self.wait_for_id(element_id='_mainContentPlaceHolder_accountTransactions' \
                                    'Ctrl00__accountSelectTable',
                         error_message='Could not connect')

        select = Select(self.driver \
                .find_element_by_name('ctl00$_mainContentPlaceHolder$account' \
                                      'TransactionsCtrl00$_listOfAccounts'))
        for o in select.options:
            value = o.get_attribute('value')
            if re.match(r'\d+\|%s\|' % number.replace('-', ''), value):
                select.select_by_value(value)
                break

        self.wait_for_id(element_id='_mainContentPlaceHolder_accountTransactions' \
                                    'Ctrl00__accountTransactionsList',
                        error_message='Could not connect')


    def get_account(self, number):
        """ Get account details """
        self._go_to_portfolio()
        self._go_to_manage_accounts()
        self._go_to_accounts()

        self.driver.find_element_by_link_text(u'%s' % number).click()
        self.wait_for_id(element_id='_mainContentPlaceHolder_accountDetails' \
                                    'Ctrl00__productContent',
                         error_message='Could not connect')

        html = self.driver.find_element_by_id('_mainContentPlaceHolder_account' \
                                              'DetailsCtrl00__productContent') \
                .get_attribute('innerHTML')

        parser = WinbankHtmlParser(html)
        return parser.get_account(number)

    def get_transactions(self, number):
        self._go_to_portfolio()
        self._go_to_manage_accounts()
        self._go_to_transactions(number)

        html = self.driver.find_element_by_id('_mainContentPlaceHolder_accountTransactions' \
                                              'Ctrl00__accountTransactionsList') \
                .get_attribute('innerHTML')

        parser = WinbankHtmlParser(html)
        return parser.get_transactions()

    def logout(self):
        self.driver.find_element_by_id('_headerControl__logoffImageButton').click()
        self.wait_for_id(element_id='reconnectLink',
                         error_message='Could not connect')


class WinbankHtmlParser(object):
    # Map account table columns to structured data
    __ACCOUNT_MAP__ = {
        'IBAN': {
            'label': u'ΙΒΑΝ Απεικόνιση:',
            'replacements': [[r'\s', '']]
        },
        'type': {
            'label': u'Είδος:'
        },
        'balance': {
            'label': u'Λογιστικό:',
            'replacements': [[r'\.', ''], [r',', '.'], [r'\s+EUR', '']]
        }
    }

    # Map transaction table columns to structured data
    # The index in this list corresponds to the element
    # index in html 
    __TRANSACTIONS_MAP__ = [
            ('posted', '_get_transaction_date_table'),
            ('completed', '_get_transaction_date'),
            ('description', '_get_transaction_column'),
            ('comment', '_get_transaction_comment'),
            ('value_amount', '_get_transaction_amount'),
            ('transaction_id', '_get_transaction_column'),
    ]

    def __init__(self, html_string):
        self.tree = BeautifulSoup(html_string, 'html.parser')

    def _get_account_value(self, mappings):
        td = self.tree.find('td',
                string=re.compile(ur'%s' % mappings['label'])).find_next()

        try:
            value = td.text.strip()
        except:
            value = ''
        else:
            if 'replacements' in mappings and len(value):
                for replacement in mappings['replacements']:
                    value = re.sub(replacement[0], replacement[1], value)

        return value

    def _get_transaction_date_table(self, td):
        return datetime.strptime(td.find('table').find_all('td')[1].text.strip(),
                                 '%d/%m/%Y').replace(tzinfo=utc)

    def _get_transaction_date(self, td):
        return datetime.strptime(td.text.strip(), '%d/%m/%Y').replace(tzinfo=utc)

    def _get_transaction_column(self, td):
        return td.text.strip()

    def _get_transaction_amount(self, td):
        value = re.sub(r'\.', '', td.text.strip())
        value = re.sub(r',', '.', value)
        return Decimal(re.sub(r'\s+EUR', '', value))

    def _get_transaction_comment(self, td):
        return td.decode_contents(formatter="html").strip()

    def _get_transaction(self, tr):
        ret = {'type': 'cash', 'value_currency': 'EUR', 'status': 'APPROVED',
               'this_account_type': 'bank'}

        for i, td in enumerate(tr.find_all('td', recursive=False)):
            if len(self.__TRANSACTIONS_MAP__) > i:
                map_tuple = self.__TRANSACTIONS_MAP__[i]
                try:
                    ret[map_tuple[0]] = getattr(self, map_tuple[1])(td)
                except AttributeError:
                    # this is not a transaction row
                    if i == 0:
                        return None
                    ret[map_tuple[0]] = ''

        return ret

    def get_account(self, number):
        """ Account details """
        ret = {'number': '%s' % number, 'currency': 'EUR'}

        for key, mapping in self.__ACCOUNT_MAP__.iteritems():
            ret[key] = self._get_account_value(mapping)

        ret['balance'] = Decimal(ret['balance'])
        return ret

    def get_transactions(self):
        """ Transaction details """
        transactions = []
        for i, tr in enumerate(self.tree.tbody.find_all('tr', recursive=False)):
            # the first line contains the headers
            if i:
                transaction = self._get_transaction(tr)
                if transaction:
                    transactions.append(transaction) 
        return transactions
