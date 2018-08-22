import json
import logging
import urllib.request
from datetime import datetime, timedelta

from pysmoothstreams import Service, LIVE247, MMATV


class AuthSign:
	def __init__(self, service=LIVE247, auth=(None, None)):
		self.service = self.__set_service(service)
		self.username = auth[0]
		self.password = auth[1]

		self.expiration_date = None
		self.hash = None

		if self.service == MMATV:
			self.url = 'https://www.MMA-TV.net/loginForm.php'
		else:
			self.url = 'https://auth.smoothstreams.tv/hash_api.php'

	def __set_service(self, service):
		if not isinstance(service, Service):
			raise TypeError(f'{service} is not a valid service!')
		return service

	def fetch_hash(self):
		now = datetime.now()

		if self.username is not None and self.password is not None:

			if self.hash is None or now > self.expiration_date:
				logging.warning('Hash is either none or may be expired. Getting a new one...')
				hash_url = f'{self.url}?username={self.username}&password={self.password}&site={self.service.site}'
				# logging.info(f'Fetching hash at {hash_url}')

				with urllib.request.urlopen(hash_url) as response:

					try:
						as_json = json.loads(response.read())

						if 'hash' in as_json:
							self.hash = as_json['hash']
							self.set_expiration_date(as_json['valid'])

					except Exception as e:
						print('error!')

			logging.info(f'Returning hash {self.hash}')
			return self.hash

		else:
			raise ValueError('Username or password is not set.')

	def set_expiration_date(self, minutes):
		now = datetime.now()
		self.expiration_date = now + timedelta(minutes=minutes - 1)
		logging.info(f'Expiration date set to {self.expiration_date}')
