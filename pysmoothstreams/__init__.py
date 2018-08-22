from collections import namedtuple
from enum import Enum


class Feed(Enum):
	SMOOTHSTREAMS = 'https://fast-guide.smoothstreams.tv/feed.json'
	FOG = 'https://fast-guide.smoothstreams.tv/altepg/feedall1.json'


class Quality(Enum):
	HD = 1
	HQ = 2
	LQ = 3


class Protocol(Enum):
	HLS = 'https'
	RTMP = 'rtmp'


class Server(Enum):
	EU_MIX = 'deu.smoothstreams.tv'

	EU_DE_MIX = 'deu-de.smoothstreams.tv'

	EU_NL_MIX = 'deu-nl.smoothstreams.tv'
	EU_NL1 = 'deu-nl1.smoothstreams.tv'
	EU_NL2 = 'deu-nl2.smoothstreams.tv'
	EU_NL3 = 'deu-nl3.smoothstreams.tv'
	EU_NL4 = 'deu-nl4.smoothstreams.tv'
	EU_NL5 = 'deu-nl5.smoothstreams.tv'

	EU_UK_MIX = 'deu-uk.smoothstreams.tv'
	EU_UK1 = 'deu-uk1.smoothstreams.tv'
	EU_UK2 = 'deu-uk2.smoothstreams.tv'

	NA_EAST_MIX = 'dna.smoothstreams.tv'
	NA_WEST_MIX = 'dnaw.smoothstreams.tv'

	NA_EAST_NJ = 'dnae1.smoothstreams.tv'
	NA_EAST_VA = 'dnae2.smoothstreams.tv'
	NA_EAST_MTL = 'dnae3.smoothstreams.tv'
	NA_EAST_TOR = 'dnae4.smoothstreams.tv'
	NA_EAST_NY = 'dnae6.smoothstreams.tv'

	NA_WEST_PHX = 'dnaw1.smoothstreams.tv'
	NA_WEST_LA = 'dnaw2.smoothstreams.tv'
	NA_WEST_CHI_1 = 'dnaw3.smoothstreams.tv'
	NA_WEST_CHI_2 = 'dnaw4.smoothstreams.tv'

	ASIA_SING = 'dap.smoothstreams.tv'


Service = namedtuple('Service', 'site rtmp_port hls_port')
LIVE247 = Service('view247', 3625, 443)
STARSTREAMS = Service('viewss', 3665, 443)
STREAMTVNOW = Service('viewstvn', 3615, 443)
MMATV = Service('viewmmasr', 3635, 443)
