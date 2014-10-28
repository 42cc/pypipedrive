# coding: utf-8
import logging

import requests
from os import environ

PIPEDRIVE_API_URL = 'https://api.pipedrive.com/v1/'


logger = logging.getLogger('pypipedrive')


class PipeDriveError(StandardError):
    pass


class APIPipedError(PipeDriveError):

    def __init__(self, value):
        self.value = value['error']

    def __str__(self):
        return repr(self.value)


class BasePipedError(PipeDriveError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Method(object):
    custom_method = {}

    @classmethod
    def custom(self, *methodNames):
        def call(f):
            for methodName in methodNames:
                self.custom_method[methodName] = f
        return call

    @classmethod
    def get(self, piped, methodName):
        if methodName in self.custom_method:
            return self.custom_method[methodName](piped, methodName)
        else:
            return self(piped, methodName)

    def __init__(self, piped, method_name):
        self.piped = piped
        self.method_name = method_name

    def __getattr__(self, key):
        return Method.get(self.piped, '.'.join((self.method_name, key)))

    def __call__(self, **kwargs):
        return self.piped.get_response(base_url=self.method_name, **kwargs)


class PipeDrive(object):

    def __init__(self, api_token):
        self.api_token = api_token
        self.api_url = PIPEDRIVE_API_URL
        self.default_params = {}
        self.session = requests.Session()
        self.session.headers['X-API-Token'] = api_token

    def __getattr__(self, key):
        return Method(self, key)

    def get_response(self, base_url, **kwargs):
        base = base_url.split('.')
        base = '/'.join([self.format_url_attr(s, kwargs) for s in base])
        params = dict(
            (k, v) for k, v in kwargs.iteritems() if not k.startswith('_'))
        if 'method' in params:
            method = params['method']
            del params['method']
        else:
            method = 'GET'
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise BasePipedError(u'The method is not specified correctly')
        logger.debug(
            '{method} {url}, params: {params}'.format(
                method=method,
                url="%s%s" % (self.api_url, base),
                params=params))
        # Merge the user settings with default settings and exec
        query_params = dict(self.default_params, **params)
        url = "%s%s" % (self.api_url, base)
        if method == 'GET':
            r = self.session.get(url, params=query_params)
        else:
            r = getattr(self.session, method.lower())(url, data=query_params)
        response = r.json()
        if 'error' in response:
            raise APIPipedError(response)
        return response

    def format_url_attr(self, str, params):
        if str.startswith('_'):
            if str in params:
                return (params[str])
        return str


if __name__ == "__main__":
    api_token = environ.get('PIPEDRIVE_API_TOKEN')
    p = PipeDrive(api_token)
    r = p.persons(limit=5)
    print r
