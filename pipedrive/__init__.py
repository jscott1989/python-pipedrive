from httplib2 import Http

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import json
from copy import copy

PIPEDRIVE_API_URL = "https://api.pipedrive.com/v1/"

class PipedriveError(Exception):
    def __init__(self, response):
        self.response = response
    def __str__(self):
        return self.response.get('error', 'No error provided')

class IncorrectLoginError(PipedriveError):
    pass

class Pipedrive(object):
    def _request(self, endpoint, data, method='POST'):
        if self.api_token:
            data = copy(data)
            # data['api_token'] = self.api_token
        if method == "GET":
            print('sending GET request to ' + PIPEDRIVE_API_URL + endpoint + '?api_token=' + str(self.api_token) + '&' + urlencode(data))
            response, data = self.http.request(PIPEDRIVE_API_URL + endpoint + '?api_token=' + str(self.api_token) + '&' + urlencode(data), method=method, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response, data = self.http.request(PIPEDRIVE_API_URL + endpoint + '?api_token=' + str(self.api_token), method=method, body=urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        # print(json.dumps(json.loads(data.decode('utf-8')), sort_keys=True, indent=4))

        # if python2, use:
        # return json.loads(data)
        return json.loads(data.decode('utf-8'))

    def __init__(self, email, password = None):
        self.http = Http()
        if password:
            response = self._request("/authorizations/", {"email": email, "password": password})

            if 'error' in response:
                raise IncorrectLoginError(response)
            
            # self.api_token = response['authorization'][0]['api_token']
            self.api_token = response['data'][0]['api_token']
            print('api_token is ' + self.api_token)
        else:
            # Assume that login is actually the api token
            self.api_token = email

    def __getattr__(self, name):
        def wrapper(data, method):
            response = self._request(name.replace('_', '/'), data, method)
            if 'error' in response:
                raise PipedriveError(response)
            return response
        return wrapper
