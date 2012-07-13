from httplib2 import Http
from urllib import urlencode
import json
from copy import copy

PIPEDRIVE_API_URL = "https://api.pipedrive.com/1.0/"

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

		return json.loads(data)

	def __init__(self, login, password = None):
		self.http = Http()
		if password:
			response = self._request("/auth/login", {"login": login, "password": password})

			if 'error' in response:
				raise IncorrectLoginError(response)
			
			self.api_token = response['authorization'][0]['api_token']
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
