import logging
import time
import sys
import os

import jwt
import requests
import six


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '[%(levelname)s]%(asctime)-15s %(filename)s %(lineno)d: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
log = logging.getLogger(__name__)


class BigObject(object):

    def __init__(self, obj, name='BigObject'):
        assert isinstance(obj, dict), 'obj must be a dict instance'
        self._origin = obj
        self._name = name.capitalize() if name else None
        for key, value in self._origin.items():
            if isinstance(value, dict):
                self._origin[key] = BigObject(value, key)
            elif isinstance(value, list):
                self._origin[key] = PaginatedResult(value, key)
    
    def __getattr__(self, name):
        if name in self._origin:
            return self._origin[name]
        raise AttributeError(
            "%s object has no attribute '%s'" % (self._name, name)
        )
    
    def __dir__(self):
        return self._origin.keys()

    def __repr__(self):
        if six.PY2:
            values = []
            for k, v in self._origin.items():
                k = k.encode('utf-8')
                if six.PY2 and isinstance(v, unicode):
                    v = v.encode('utf-8')
                else:
                    v = repr(v)
                values.append('%s: %s' % (k, v))
            values = ','.join(values)
            return '<%s (%s)>' % (self._name.encode('utf-8'), values)
        values = ','.join(['%s: %s' % (k, v) for k,v in self._origin.items()])
        return '<%s (%s)>' % (self._name, values)
    
    def __str__(self):
        return repr(self)
    
    def __unicode__(self):
        return repr(self).decode('utf-8')


class PaginatedResult(object):
    
    def __init__(self, response, result_type='BigObject'):
        if 'page_info' in response:
            self.page_info = response['page_info']
        else:
            self.page_info = {}
        data = []
        if 'edges' in response:
            for item in response['edges']:
                obj = {}
                obj.update(item['node'])
                if 'cursor' in item:
                    obj['cursor'] = item['cursor']
                data.append(BigObject(obj, result_type))
        else:
            data = [BigObject(obj, result_type) for obj in response]
        self.data = data
        self._index = 0
        self.result_type = result_type
    
    def __iter__(self):
        while self._index < len(self.data):
            yield self.data[self._index]
            self._index += 1
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __repr__(self):
        return '<CollectionResult[%s], %d records.> : %s' % (
            self.result_type, len(self.data), self.data)
        
    @property
    def has_next_page(self):
        return self.page_info.get('has_next_page', False)
    
    @property
    def has_previous_page(self):
        return self.page_info.get('has_previous_page', False)
    
    @property
    def start_cursor(self):
        return self.page_info.get('start_cursor', None)
    
    @property
    def end_cursor(self):
        return self.page_info.get('end_cursor', None)
    

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

    def __init__(self, api, secret, entry_point='https://big.one/api/v2/',
                 limit_rate=True, limiter=None, raw_response=False):
        if not entry_point.endswith('/'):
            entry_point = entry_point + '/'
        self.api = api
        self.secret = secret
        self.entry_point = entry_point
        self.limit_rate = limit_rate
        self.raw_response = raw_response
        self.ping()
    
    def ping(self):
        return self.public_get('ping')

    @property
    def header(self):
        return {
            'Authorization': 'Bearer %s' % signature(self.api, self.secret)
        }

    def send_request(self, url, method='GET', result_type='BigObject',
                     parameters=None, headers=None):
        url = self.entry_point + url
        url = url.strip()
        log.info('sending request : %s' % url)
        if method == 'GET':
            rsp = requests.get(url, params=parameters, headers=headers)
        elif method == 'POST':
            rsp = requests.post(url, data=parameters, headers=headers)
        else:
            log.error('unsupport request method : %s' % method)
            raise ValueError('unsupport HTTP method %s' % method)
        if str(rsp.status_code).startswith('2'):
            data = rsp.json()
            log.debug('reponse data:')
            log.debug(data)
            ret = None
            if 'errors' in data:
                error = data['errors'][0]
                if 'code' in error:
                    raise BigOneAPIException(error['code'], error['message'])
                elif 'message' in error:
                    log.warning('error respone without code, b1 making mistake')
                    raise BigOneAPIException(-1, error['message'])
                else:
                    raise BigOneRequestException(
                        'unrecognized response %s' % data
                    )
                    
            elif 'data' in data:
                log.debug('success response')
                ret = data['data']
            else:
                log.debug('not a regular response')
                ret = data
            
            if self.raw_response:
                log.info('raw_response enable')
                return ret
            if 'edges' not in ret and not isinstance(ret, list):
                log.debug('The result is a dict')
                return BigObject(ret, result_type)
            log.debug('The result is a list')
            return PaginatedResult(ret, result_type)

        else:
            raise BigOneRequestException(
                'bad request with error respone code %d' % rsp.status_code)

    def public_get(self, url, result_type='BigObject', parameters=None):
        return self.send_request(url, 'GET', result_type, parameters)

    def public_post(self, url, result_type='BigObject', parameters=None):
        return self.send_request(url, 'POST', result_type, parameters)
    
    def private_get(self, url, result_type='BigObject', parameters=None):
        return self.send_request(url, 'GET', result_type, parameters, self.header)
    
    def private_post(self, url, result_type='BigObject', parameters=None):
        return self.send_request(url, 'POST', result_type, parameters, self.header)
