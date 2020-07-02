from enum import Enum


class Feed(Enum):
    SMOOTHSTREAMS = 'https://fast-guide.smoothstreams.tv/feed.xml'
    ALTEPG = 'https://fast-guide.smoothstreams.tv/altepg/xmltv1.xml.gz'


class Quality(Enum):
    HD = 1
    HQ = 2
    LQ = 3

    def __str__(self):
        return str(self.value)


class Protocol(Enum):
    HLS = 1
    RTMP = 2
    MPEG = 3

    def __str__(self):
        return self.value


class Server(Enum):
    EU_MIX = 'deu.smoothstreams.tv'  # European Server Mix

    EU_DE_MIX = 'deu-de.smoothstreams.tv'  # European DE Mix
    EU_DE1 = 'deu-de1.smoothstreams.tv'  # European DE1 (DP)

    EU_NL_MIX = 'deu-nl.smoothstreams.tv'  # European NL Mix
    EU_NL1 = 'deu-nl1.smoothstreams.tv'  # European NL1 (i3d)

    EU_UK_MIX = 'deu-uk.smoothstreams.tv'  # European UK Mix
    EU_UK1 = 'deu-uk1.smoothstreams.tv'  # European UK1 (io)
    EU_UK2 = 'deu-uk2.smoothstreams.tv'  # European UK2 (100TB)

    EU_FR_MIX = 'deu-fr.SmoothStreams.tv'  # European FR Mix (DP)
    EU_FR1 = 'deu-fr1.smoothstreams.tv'  # European FR1 (DP)

    NA_MIX = 'dna.smoothstreams.tv'  # US/CA Server Mix

    NA_EAST_MIX = 'dnae.smoothstreams.tv'  # US/CA East Server Mix
    NA_EAST_NJ = 'dnae1.smoothstreams.tv'  # US/CA East 1 (NJ)
    NA_EAST_NY = 'dnae2.smoothstreams.tv'  # US/CA East 2 (NY)
    NA_EAST_CHI = 'dnae3.smoothstreams.tv'  # US/CA East 3 (CHI)
    NA_EAST_ATL = 'dnae4.smoothstreams.tv'  # US/CA East 4 (ATL)
    NA_EAST_VA = 'dnae5.SmoothStreams.tv'  # US/CA East 5 (VA)

    NA_WEST_MIX = 'dnaw.smoothstreams.tv'  # US/CA West Server Mix
    NA_WEST_LA = 'dnaw1.smoothstreams.tv'  # US/CA West 1 (LA)
    NA_WEST_AZ = 'dnaw2.smoothstreams.tv'  # US/CA West 2 (AZ)

    ASIA_MIX = 'dAP.smoothstreams.tv'  # Asia - Mix
    ASIA_SG_01 = 'dAP1.smoothstreams.tv'  # Asia - SG 1 (SL)
    ASIA_SG_02 = 'dAP2.smoothstreams.tv'  # Asia - SG 2 (OVH)
    ASIA_SG_03 = 'dAP3.smoothstreams.tv'  # Asia - SG 3 (DO)

    def __str__(self):
        return self.value


class Service(Enum):
    LIVE247 = 'view247'
    STARSTREAMS = 'viewss'
    STREAMTVNOW = 'viewstvn'
    MMATV = 'viewmmasr'
