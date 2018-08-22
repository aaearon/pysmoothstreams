from enum import Enum


class Feed(Enum):
	SMOOTHSTREAMS = 'https://fast-guide.smoothstreams.tv/feed.json'
	FOG = 'https://fast-guide.smoothstreams.tv/altepg/feedall1.json'


class Quality(Enum):
	HD = 1
	HQ = 2
	LQ = 3


class Site(Enum):
	MYSTREAMS = 'viewms'
	LIVE247 = 'view247'
	STARSTREAMS = 'viewss'
	STREAMTVNOW = 'viewstvn'
	MMATV = 'viewmmasr'
