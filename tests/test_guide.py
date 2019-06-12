from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pysmoothstreams import LIVE247, Server, Quality, Protocol, STREAMTVNOW
from pysmoothstreams.auth import AuthSign
from pysmoothstreams.exceptions import InvalidServer, InvalidQuality, InvalidProtocol
from pysmoothstreams.guide import Guide


class TestGuide(TestCase):
    def test__build_stream_url_live247_rtmp(self):
		a = AuthSign(service=LIVE247, auth=('fake', 'fake'))
		# set hash and expiration manually
		a.expiration_date = datetime.now() + timedelta(minutes=240)
		a.hash = 'abc1234'

		g = Guide()
		generated = g._build_stream_url(Server.NA_EAST_VA, 44, a, Quality.HD, Protocol.RTMP)

		self.assertEqual(
			'rtmp://dnae2.smoothstreams.tv:3625/view247/ch44q1.stream/playlist.m3u8?wmsAuthSign=abc1234', generated)

    def test__build_stream_url_streamtvnow_hls(self):
		a = AuthSign(service=STREAMTVNOW, auth=('fake', 'fake'))
		# set hash and expiration manually
		a.expiration_date = datetime.now() + timedelta(minutes=240)
		a.hash = 'abc1234'

        g = Guide()
        generated = g._build_stream_url(Server.NA_EAST_VA, 3, a, Quality.LQ, Protocol.HLS)

		self.assertEqual(
            'https://dnea2.smoothstreams.tv:443/viewstvn/ch03q3.stream/playlist.m3u8?wmsAuthSign=abc1234', generated)

    def test__build_stream_url_streamtvnow_mpeg(self):
        a = AuthSign(service=STREAMTVNOW, auth=('fake', 'fake'))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = 'abc1234'

        g = Guide()
        generated = g._build_stream_url(Server.EU_MIX, 3, a, Quality.LQ, Protocol.MPEG)

        self.assertEqual('https://deu.smoothstreams.tv:443/viewstvn/ch03q3.stream/mpeg.2ts?wmsAuthSign=abc1234',
                         generated)

	def test_generate_streams(self):
		a = AuthSign(service=STREAMTVNOW, auth=('fake', 'fake'))
		g = Guide()

		with self.assertRaises(InvalidServer) as context:
			g.generate_streams('FakeServer', Quality.HD, a, protocol=Protocol.HLS)

		self.assertTrue('FakeServer is not a valid server!' in str(context.exception))

		with self.assertRaises(InvalidQuality) as context:
			g.generate_streams(Server.EU_MIX, 29, a, protocol=Protocol.HLS)

		self.assertTrue('29 is not a valid quality!' in str(context.exception))

		with self.assertRaises(InvalidProtocol) as context:
			g.generate_streams(Server.EU_MIX, Quality.LQ, a, protocol='abc')

		self.assertTrue('abc is not a valid protocol!' in str(context.exception))

	@patch('urllib.request.urlopen')
	def test__fetch_channels(self, mock_urlopen):
		with open('test_feed.json') as f:
			json_feed = f.read()

		cm = MagicMock()
		cm.getcode.return_value = 200
		cm.read.return_value = json_feed
		cm.info.return_value = {'Expires': 'Sat, 25 Aug 2018 22:39:41 GMT'}
		cm.__enter__.return_value = cm
		mock_urlopen.return_value = cm

		g = Guide()
		self.assertEqual(150, len(g.channels))

    # with open('test_feed.xml') as f:
    # 	xml_feed = f.read()
    #
    # cm = MagicMock()
    # cm.getcode.return_value = 200
    # cm.read.return_value = xml_feed
    # cm.info.return_value = {'Expires': 'Sat, 25 Aug 2018 22:39:41 GMT'}
    # cm.__enter__.return_value = cm
    # mock_urlopen.return_value = cm

# g = Guide(feed='https://fast-guide.smoothstreams.tv/feed.xml')
# self.assertEqual(150, len(g.channels))
