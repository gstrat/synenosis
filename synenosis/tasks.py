from celery import states, task
from celery.exceptions import Ignore
from .importers.winbank import WinbankConnector
from .importers.nbg import NBGConnector
from .importers.paypalnvp import PayPalConnector
from .importers.exceptions import ConnectorError
from .models import Institution
from synenosis.models import BankAccount, Transaction, WalletAccount


def _store_account(ttask, inst, account):
    ttask.update_state(state='PROGRESS', # @UndefinedVariable
            meta={'message': 'Importing account...', 'progress': 55})

    account['institution'] = inst
    ba = BankAccount.objects.create(**account)

    ttask.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Retrieving transactions...', 'progress': 66})

    return ba


def _store_transactions(ttask, ba, transactions):
    """ Store the transactions """
    ttask.update_state(state='PROGRESS', # @UndefinedVariable
            meta={'message': 'Importing transactions...', 'progress': 90})

    t_to_store = []
    for t in transactions:
        t['this_account'] = ba.account_id
        t_to_store.append(Transaction(**t))

    if len(t_to_store):
        Transaction.objects.bulk_create(t_to_store)

    ttask.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Finalizing import...', 'progress': 99})


@task(bind=True)
def import_winbank(self, username, password, number):
    """ Import a winbank account & transactions """
    inst = Institution.objects.get(short_name='PIRBGRAA')

    win = WinbankConnector()
    self.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Attempting to login...', 'progress': 10})

    try:
        win.login(username, password)
    except ConnectorError:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Your credentials were invalid'})
        raise Ignore()

    self.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Retrieving account information...', 'progress': 33})

    try:
        account = win.get_account(number)
    except ConnectorError:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Invalid bank account'})
        raise Ignore()

    from logging import getLogger
    logger = getLogger(__name__)
    logger.warning('%s' % account)

    ba = _store_account(self, inst, account)

    try:
        transactions = win.get_transactions(number)
    except ConnectorError:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Connection error'})
        raise Ignore()
    else:
        _store_transactions(self, ba, transactions)

    return True



@task(bind=True)
def import_nbg(self, key, account_id):
    """ Import an NBG account & transactions """
    inst = Institution.objects.get(short_name='ETHNGRAA')

    nbg = NBGConnector(key)

    self.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Retrieving account information...', 'progress': 33})

    try:
        account = nbg.get_account(account_id)
    except:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Invalid credentials'})
        raise Ignore()

    ba = _store_account(self, inst, account)

    try:
        transactions = nbg.get_transactions(account_id)
    except ConnectorError:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Connection error'})
        raise Ignore()
    else:
        _store_transactions(self, ba, transactions)

    return True


@task(bind=True)
def import_paypal(self, username, password, signature):
    inst = Institution.objects.get(short_name='PAYPAL')
    
    nbg = PayPalConnector(username=username,
                       password=password,
                       signature=signature)

    self.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Retrieving account information...', 'progress': 33})

    try:
        account = nbg.get_account()
    except:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Invalid credentials'})
        raise Ignore()

    self.update_state(state='PROGRESS', # @UndefinedVariable
            meta={'message': 'Importing account...', 'progress': 55})

    account['institution'] = inst
    ba = WalletAccount.objects.create(**account)

    self.update_state(state='PROGRESS', # @UndefinedVariable
        meta={'message': 'Retrieving transactions...', 'progress': 66})

    try:
        transactions = nbg.get_transactions()
    except ConnectorError:
        self.update_state(state=states.SUCCESS, meta={'fmessage': 'Connection error'})
        raise Ignore()
    else:
        _store_transactions(self, ba, transactions)

    return True
