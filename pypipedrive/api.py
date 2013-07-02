# coding: utf-8

import requests
from os import environ

PIPEDRIVE_API_URL = 'https://api.pipedrive.com/v1/'


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
        self.default_params = {'api_token': api_token}

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
        # Merge the user settings with default settings and exec
        query_params = dict(self.default_params, **params)
        if method == 'GET':
            url = "%s%s" % (self.api_url, base)
            r = requests.get(url, params=query_params)
        else:
            url = "%s%s?api_token=%s" % \
                (self.api_url, base, query_params['api_token'])
            del query_params['api_token']
            r = getattr(requests, method.lower())(url, data=query_params)
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
