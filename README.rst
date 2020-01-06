pysmoothstreams
===============
A Python library for working with SmoothStreams services.

Usage
-----
Create a list of channels with metadata -- including stream URLs -- for a defined service, for a particular server, with a specific quality.

    >>> g = Guide(Feed.ALTEPG)
    >>> auth = AuthSign(service=Service.LIVE247, auth=('username', 'password'))
    'c2VydmVyX3R...'
    >>> s = g.generate_streams(Server.NA_EAST_VA, Quality.HD, auth, Protocol.RTMP)
    >>> s[0]
    {'number': '1', 'name': '01 - ESPNNews', 'icon': 'https://fast-...', 'url': 'rtmp://dnae2.smoothstreams.tv:3625/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=c2VydmVyX3R...'}
    >>> s[0]['url']
    'rtmp://dnae2.smoothstreams.tv:3625/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=c2VydmVyX3R...'