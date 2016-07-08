from httplib2 import Http

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import json
from copy import copy

PIPEDRIVE_API_URL = "https://api.pipedrive.com/v1"

class PipedriveError(Exception):
	def __init__(self, response):
		self.response = response
	def __str__(self):
		return self.response.get('error', 'No error provided')

class IncorrectLoginError(PipedriveError):
	pass

class Pipedrive(object):
	def _request(self, endpoint, data, method="POST"):
		if self.api_token:
			data = copy(data)
			data['api_token'] = self.api_token
		response, data = self.http.request(PIPEDRIVE_API_URL + endpoint, method=method, body=urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})

		# if python2, use:
		# return json.loads(data)
		return json.loads(data.decode('utf-8'))

	def __init__(self, email, password = None):
		self.http = Http()
		if password:
			response = self._request("/authorizations/", {"email": email, "password": password})
			

			print(json.dumps(response, sort_keys=True, indent=4))

			if 'error' in response:
				raise IncorrectLoginError(response)
			
			# self.api_token = response['authorization'][0]['api_token']
			self.api_token = response['data'][0]['api_token']
			print('api_token is ' + self.api_token)
		else:
			# Assume that login is actually the api token
			self.api_token = login

	def __getattr__(self, name):
		def wrapper(data):
			response = self._request(name.replace('_', '/'), data)
			if 'error' in response:
				raise PipedriveError(response)
			return response
		return wrapper
