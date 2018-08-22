import json
import logging
import urllib.request
from datetime import datetime, timedelta

from pysmoothstreams import Site


class AuthSign:
	def __init__(self, site=Site.LIVE247, auth=(None, None)):
		self.site = site.value
		self.username = auth[0]
		self.password = auth[1]

		self.expiration_date = None
		self.hash = None

		if self.site == 'viewmmasr':
			self.url = 'https://www.MMA-TV.net/loginForm.php'
		else:
			self.url = 'https://auth.smoothstreams.tv/hash_api.php'

	def fetch_hash(self):
		now = datetime.now()

		if self.username is not None and self.password is not None:

			if self.hash is None or now > self.expiration_date:
				logging.info('Hash is either none or may be expired. Getting a new one...')
				hash_url = f'{self.url}?username={self.username}&password={self.password}&site={self.site}'

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
