import time
import jwt
import requests


def signature(api, secret):
    payload = {
        'type': 'OpenAPI',
        'sub': api,
        'nonce': int(time.time() * 10e8)
    }
    encoded = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
    return encoded


class BigOneAPIException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message


class BigOneRequestException(Exception):
    pass

class Request(object):

    def __init__(self, api, secret, entry_point, limit_rate, limiter):
        self.api = api
        self.secret = secret
        self.entry_point = entry_point
        self.limit_rate = limit_rate

    @property
    def header(self):
        return {
            'Authorization': 'Bearer %s' % signature(self.api, self.secret)
        }

    def send_request(self, url, method='GET', parameters=None, headers=None):
        url = self.entry_point + url
        if method == 'GET':
            rsp = requests.get(url, params=parameters, headers=headers)
        elif method == 'POST':
            rsp = requests.post(url, data=parameters, headers=headers)
        else:
            raise ValueError('unsuport HTTP method %s' % method)
        if str(rsp.status_code).startswith('2'):
            data = rsp.json()
            if 'errors' in data:
                error = data['errors'][0]
                raise BigOneAPIException(error['code'], error['message'])
            return rsp.json()['data']
        else:
            raise BigOneRequestException(
                'bad request with error respone code %d' % rsp.status_code)

    def public_get(self, url, parameters=None):
        return self.send_request(url, 'GET', parameters)

    def public_post(self, url, parameters=None):
        return self.send_request(url, 'POST', parameters)
    
    def private_get(self, url, parameters=None):
        return self.send_request(url, 'GET', parameters, self.header)
    
    def private_post(self, url, parameters=None):
        return self.send_request(url, 'POST', parameters, self.header)
