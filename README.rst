pysmoothstreams
===============
A Python library for working with SmoothStreams services.

Note: Only generates HLS streams at the moment.

Usage
----
Create a list of channels with metadata -- including stream URLs -- for a defined service, for a particular server, with a specific quality.

    >>> g = Guide(Feed.FOG)
    >>> auth = AuthSign(service=LIVE247, auth=('username', 'password'))
    'c2VydmVyX3R...'
    >>> s = g.generate_streams(Server.NA_EAST_VA, Quality.HD, auth)
    >>> s[0]
    {'number': '1', 'name': '01 - ESPNNews', 'icon': 'https://fast-...', 'url': 'https://dnae2.smoothstreams.tv/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=c2VydmVyX3R...'}
    >>> s[0]['url']
    'https://dnae2.smoothstreams.tv/view247/ch01q1.stream/playlist.m3u8?wmsAuthSign=c2VydmVyX3R...'