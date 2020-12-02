from pysmoothstreams import Server, Quality, Protocol, Service, Feed


class Playlist:
    def __init__(self, auth_sign, guide):
        self.auth_sign = auth_sign
        self.guide = guide

        self.channels = guide.channels

    def generate_m3u_playlist(
        self, server, auth_sign, quality=Quality.HD, protocol=Protocol.HLS
    ):
        playlist = "#EXTM3U\n"
        for channel in self.channels:
            clean_channel_name = channel["name"].strip()

            playlist += '#EXTINF: tvg-id="{channel_id}" tvg-name="{clean_channel_name}" tvg-logo="{channel_icon}" tvg-chno="{channel_number}", {clean_channel_name}\n'.format(
                channel_id=channel["id"],
                clean_channel_name=clean_channel_name,
                channel_icon=channel["icon"],
                channel_number=channel["number"],
            )
            playlist += "{url}\n".format(
                url=self.guide.build_stream_url(
                    server, channel["number"], auth_sign, quality, protocol
                )
            )
        return playlist
