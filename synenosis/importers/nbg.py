from decimal import Decimal
import httplib, urllib, json, datetime


class NBGConnector(object):
    """ Connect to the nbg api """
    base_url = ''

    def __init__(self, key):
        self.key = key

    def _get_headers(self):
        return {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '%s' % self.key,
        }

    def _encode_params(self, params):
        if params:
            return urllib.urlencode(params)
        return ''

    def _post(self, url, params={}, body={}):
        try:
            conn = httplib.HTTPSConnection('nbgdemo.azure-api.net')
            conn.request("POST", "/nodeopenapi/api/%s?%s" % \
                         (url, self._encode_params(params)),
                         json.dumps(body), self._get_headers())
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        else:
            return json.loads(data)

    def _get(self, url, params={}):
        try:
            conn = httplib.HTTPSConnection('nbgdemo.azure-api.net')
            conn.request("GET", "/nodeopenapi/api/%s?%s" % \
                         (url, self._encode_params(params)),
                         '', self._get_headers())
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        else:
            return json.loads(data)

    def get_account(self, account_id):
        response = self._post('/accounts/rest', {}, {
                'nbgtrackid': account_id,
                'payload': {
                    'id': account_id
                }
        })

        account = response['accounts'][0]

        return {
            'account_id': account_id,
            'label': account['label'],
            'number': account['number'], 
            'balance': account['balance'],
            'currency': 'EUR',
            'IBAN': account['IBAN'],
            'type': account['type'],
            'swift_bic': account['swift_bic']
        }

    def get_transactions(self, account_id):
        # In the context of this example, the account id
        # is not taken into consideration
        response = self._get('/accounts/rest', {})

        # here we should return the data which
        # we just fetched
        # However, because at this point in time the 
        # api does not return useful data
        # we will hard code a more useful
        # response for demo purposes

        return [{
            'type': 'cash',
            'value_currency': 'EUR',
            'status': 'APPROVED',
            'this_account_type': 'bank',
            'posted': datetime.datetime(2016, 4, 19, 0, 0, 0),
            'completed': datetime.datetime(2016, 4, 19, 0, 0, 0),
            'description': 'test descr',
            'comment': 'Comment from NBG 1',
            'value_amount': Decimal('130.32'), 
            'transaction_id': 'TRANSID1'
        },
        {
            'type': 'cash',
            'value_currency': 'EUR',
            'status': 'APPROVED',
            'this_account_type': 'bank',
            'posted': datetime.datetime(2016, 4, 17, 11, 0, 0),
            'completed': datetime.datetime(2016, 4, 17, 11, 0, 0),
            'description': 'test descr 2',
            'comment': 'Comment from NBG 2',
            'value_amount': Decimal('-40.32'), 
            'transaction_id': 'TRANSID2'
        },
                {
            'type': 'cash',
            'value_currency': 'EUR',
            'status': 'APPROVED',
            'this_account_type': 'bank',
            'posted': datetime.datetime(2016, 4, 17, 11, 0, 0),
            'completed': datetime.datetime(2016, 4, 17, 13, 0, 0),
            'description': 'test descr 3',
            'comment': 'Comment from NBG 3',
            'value_amount': Decimal('440.32'), 
            'transaction_id': 'TRANSID3'
        },
        {
            'type': 'cash',
            'value_currency': 'EUR',
            'status': 'APPROVED',
            'this_account_type': 'bank',
            'posted': datetime.datetime(2016, 4, 2, 0, 0, 0),
            'completed': datetime.datetime(2016, 4, 1, 0, 0, 0),
            'description': 'test descr 4',
            'comment': 'Comment from NBG 4',
            'value_amount': Decimal('30.93'), 
            'transaction_id': 'TRANSID4'
        },
        {
            'type': 'cash',
            'value_currency': 'EUR',
            'status': 'APPROVED',
            'this_account_type': 'bank',
            'posted': datetime.datetime(2016, 4, 19, 0, 0, 0),
            'completed': datetime.datetime(2016, 4, 19, 0, 0, 0),
            'description': 'test descr 5',
            'comment': 'Comment from NBG 5',
            'value_amount': Decimal('240.32'), 
            'transaction_id': 'TRANSID5'
        }
    ]
