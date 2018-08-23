from datetime import datetime, timedelta
from unittest import TestCase

from pysmoothstreams import LIVE247, Server, Quality, Protocol, STREAMTVNOW
from pysmoothstreams.auth import AuthSign
from pysmoothstreams.guide import Guide


class TestGuide(TestCase):
	def test__build_stream_url(self):
		a = AuthSign(service=LIVE247, auth=('fake', 'fake'))
		# set hash and expiration manually
		a.expiration_date = datetime.now() + timedelta(minutes=240)
		a.hash = 'abc1234'

		g = Guide()
		generated = g._build_stream_url(Server.NA_EAST_VA, 44, a, Quality.HD, Protocol.RTMP)

		self.assertEqual(
			'rtmp://dnae2.smoothstreams.tv:3625/view247/ch44q1.stream/playlist.m3u8?wmsAuthSign=abc1234', generated)

		a = AuthSign(service=STREAMTVNOW, auth=('fake', 'fake'))
		# set hash and expiration manually
		a.expiration_date = datetime.now() + timedelta(minutes=240)
		a.hash = 'abc1234'
		generated = g._build_stream_url(Server.EU_MIX, 3, a, Quality.LQ, Protocol.HLS)

		self.assertEqual(
			'https://deu.smoothstreams.tv:443/viewstvn/ch03q3.stream/playlist.m3u8?wmsAuthSign=abc1234', generated)

	def test_generate_streams(self):
		a = AuthSign(service=STREAMTVNOW, auth=('fake', 'fake'))
		g = Guide()

		with self.assertRaises(ValueError) as context:
			g.generate_streams('FakeServer', Quality.HD, a, protocol=Protocol.HLS)

		self.assertTrue('FakeServer is not a valid server!' in str(context.exception))

		with self.assertRaises(ValueError) as context:
			g.generate_streams(Server.EU_MIX, 29, a, protocol=Protocol.HLS)

		self.assertTrue('29 is not a valid quality!' in str(context.exception))
