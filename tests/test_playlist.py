from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pysmoothstreams import Server, Quality, Protocol, Service, Feed
from pysmoothstreams.auth import AuthSign
from pysmoothstreams.guide import Guide
from pysmoothstreams.playlist import Playlist


class TestGuide(TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, mock_urlopen):
        with open('./tests/test_feed.xml', 'r') as f:
            json_feed = f.read()

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = json_feed.encode()
        cm.info.return_value = {'Expires': 'Sat, 25 Aug 2018 22:39:41 GMT',
                                'Content-Type': 'text/xml'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.g = Guide(Feed.SMOOTHSTREAMS)

    @patch('urllib.request.urlopen')
    def test_generate_m3u_playlist(self, mock_urlopen):

        a = AuthSign(service=Service.LIVE247, auth=('fake', 'fake'))
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = 'abc1234'

        p = Playlist(a, self.g)

        with open('./tests/test_sample.m3u') as f:
            self.assertEqual(f.read(),
                             p.generate_m3u_playlist(Server.NA_EAST_VA, a, Quality.HD, Protocol.HLS))
