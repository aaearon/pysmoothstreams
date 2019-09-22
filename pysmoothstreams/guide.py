import logging
import urllib.request
from datetime import datetime
from io import BytesIO
from xml.etree import ElementTree
from zipfile import ZipFile

from pysmoothstreams import Feed, Quality, Server, Protocol, Service
from pysmoothstreams.exceptions import InvalidQuality, InvalidServer, InvalidProtocol, InvalidContentType


class Guide:
    def __init__(self, feed=Feed.ALTEPG):
        self.channels = []
        self.expires = None
        self.epg_data = None

        self.url = feed.value if isinstance(feed, Feed) else feed
        self._fetch_epg_data()
        self._fetch_channels()

    def _parse_expiration_string(self, expiration):
        return datetime.strptime(expiration, '%a, %d %b %Y %H:%M:%S %Z')

    def _get_content_type(self):
        head_request = urllib.request.Request(self.url, method='HEAD')

        with urllib.request.urlopen(head_request) as response:
            content_type = response.info()['Content-Type']

        return content_type

    def _fetch_zipped_feed(self):
        with urllib.request.urlopen(self.url) as response:
            self.expires = self._parse_expiration_string(response.info()['Expires'])
            logging.debug(f'Guide info set to expire in {self.expires}')

            zipped_feed = ZipFile(BytesIO(response.read()))
            for file in zipped_feed.namelist():
                b = zipped_feed.open(file).read()

        return b

    def _fetch_feed(self):
        with urllib.request.urlopen(self.url) as response:
            self.expires = self._parse_expiration_string(response.info()['Expires'])

            return response.read()

    def _fetch_epg_data(self, force=False):
        if self.expires is None or datetime.now() > self.expires or force:

            content_type = self._get_content_type()

            if content_type == 'application/zip':
                self.epg_data = self._fetch_zipped_feed()
            elif content_type == 'application/xml' or content_type == 'text/xml':
                self.epg_data = self._fetch_feed()
            else:
                raise InvalidContentType(f'Got an unexpected Content-Type: {content_type} from {self.url}')

        else:
            logging.debug('EPG data is not stale or fetched was not forced.')

    def _fetch_channels(self, force=False):

        if force:
            self._fetch_epg_data(force=True)

        self.channels = []

        tree = ElementTree.fromstring(self.epg_data)
        for index, element in enumerate(tree.iter()):
            if element.tag == 'channel':
                c = {'number': index,
                     'name': element.find('display-name').text,
                     'icon': element.find('icon').attrib['src']}
                self.channels.append(c)

            logging.debug(f'Fetched {len(self.channels)} channels.')

    def _build_stream_url(self, server, channel_number, auth_sign, quality=Quality.HD, protocol=Protocol.HLS):
        # https://dEU.smoothstreams.tv:443/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=abc1234
        # https://dEU.smoothstreams.tv:443/view247/ch01q1.stream/mpeg.2ts?wmsAuthSign=abc1234
        scheme = 'https'
        port = '443'
        playlist = 'playlist.m3u8'

        if protocol == Protocol.RTMP:
            scheme = 'rtmp'
            if auth_sign.service == Service.LIVE247:
                port = '3625'
            if auth_sign.service == Service.STARSTREAMS:
                port = '3665'
            if auth_sign.service == Service.STREAMTVNOW:
                port = '3615'
            if auth_sign.service == Service.MMATV:
                port = '3635'

        if protocol == Protocol.MPEG:
            playlist = 'mpeg.2ts'

        c = str(channel_number).zfill(2)
        logging.debug(
            f'Creating stream url with scheme "{scheme}", server "{server}", port "{port}", playlist "{playlist}"')
        stream_url = f'{scheme}://{server}:{port}/{auth_sign.service.value}/ch{c}q{quality}.stream/{playlist}?wmsAuthSign={auth_sign.fetch_hash()}'
        logging.debug(f'Stream url: {stream_url}')
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
