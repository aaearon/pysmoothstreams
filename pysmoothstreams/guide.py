import json
import logging
import urllib.request

from pysmoothstreams import Feed, Quality, Server, Protocol
from pysmoothstreams.exceptions import InvalidQuality, InvalidServer, InvalidProtocol


class Guide:
	def __init__(self, feed=Feed.SMOOTHSTREAMS):
		self.channels = []
		self.expires = None

		self.url = feed.value
		self._fetch_channels()

	def _fetch_channels(self):
		with urllib.request.urlopen(self.url) as response:
			self.expires = response.info()['Expires']
			logging.debug(f'Guide info set to expire in {self.expires}')

			try:
				as_json = json.loads(response.read())
				logging.debug(f'Retrieved {len(as_json)} channels from feed.')
				self.channels = []

				for key, value in as_json.items():
					c = {'number': value['channel_id'],
					     'name': value['name'],
					     'icon': value['img']}
					logging.debug(f'Created channel: number {c["number"]}, name {c["name"]}, icon {c["icon"]}')
					self.channels.append(c)


			except Exception as e:
				print(e.with_traceback())

		logging.debug(f'Fetched {len(self.channels)} channels.')

	def _build_stream_url(self, server, channel_number, auth_sign, quality=Quality.HD, protocol=Protocol.HLS):
		# https://dEU.smoothstreams.tv:443/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=abc1234
		port = auth_sign.service.hls_port

		if protocol == Protocol.RTMP:
			port = auth_sign.service.rtmp_port

		c = str(channel_number).zfill(2)
		stream_url = f'{protocol.value}://{server.value}:{port}/{auth_sign.service.site}/ch{c}q{quality.value}.stream/playlist.m3u8?wmsAuthSign={auth_sign.fetch_hash()}'
		return stream_url

	def generate_streams(self, server, quality, auth_sign, protocol=Protocol.HLS):
		streams = []

		if not isinstance(server, Server):
			raise InvalidServer(f'{server} is not a valid server!')

		if not isinstance(quality, Quality):
			raise InvalidQuality(f'{quality} is not a valid quality!')

		if not isinstance(protocol, Protocol):
			raise InvalidProtocol(f'{protocol} is not a valid protocol!')

		if self.channels:
			for c in self.channels:
				stream = c.copy()
				stream['url'] = self._build_stream_url(server, c['number'], auth_sign, quality, protocol)

				streams.append(stream)

			logging.info(f'Returning {len(streams)} streams.')
			return streams
