import json
import logging
import urllib.request

from pysmoothstreams import Feed, Quality


class Guide:
	def __init__(self, feed=Feed.SMOOTHSTREAMS):
		self.channels = []
		self.expires = None

		self.url = feed.value
		self._fetch_channels()

	def _fetch_channels(self):
		with urllib.request.urlopen(self.url) as response:
			self.expires = response.info()['Expires']
			logging.info(f'Guide info set to expire in {self.expires}')

			try:
				as_json = json.loads(response.read())
				self.channels = []

				for key, value in as_json.items():
					c = {'number': value['channel_id'],
					     'name': value['name'],
					     'icon': value['img']}

					self.channels.append(c)


			except Exception as e:
				print(e.with_traceback())

	def _build_stream_url(self, server, channel_number, auth_sign, quality=Quality.HD):
		# https://dEU.smoothstreams.tv:443/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=abc1234
		c = str(channel_number).zfill(2)
		stream_url = f'https://{server}/{auth_sign.site}/ch{c}q{quality}.stream/playlist.m3u8?wmsAuthSign={auth_sign.fetch_hash()}'
		return stream_url

	def generate_streams(self, server, quality, auth_sign):
		streams = []

		if self.channels:
			for c in self.channels:
				stream = c.copy()
				stream['url'] = self._build_stream_url(server, c['number'], auth_sign, quality.value)

				streams.append(stream)

			return streams
