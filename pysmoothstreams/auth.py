import json
import logging
import urllib.request
import http.cookiejar
from datetime import datetime, timedelta

from pysmoothstreams import Service
from pysmoothstreams.exceptions import InvalidService
from json import JSONDecodeError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuthSign:
    def __init__(self, service=Service.LIVE247, auth=(None, None)):
        self.service = self.__set_service(service)
        self.username = auth[0]
        self.password = auth[1]

        self.expiration_date = None
        self.hash = None

        self.url = "https://auth.smoothstreams.tv/hash_api.php"

        logger.debug(
            "Created {name} with username {username} and service {service}".format(
                name=self.__class__.__name__,
                username=self.username,
                service=self.service,
            )
        )

    def __set_service(self, service):
        if not isinstance(service, Service):
            raise InvalidService(f"{service} is not a valid service!")
        return service

    def _get_hash_via_hash_api(self):
        logger.debug("Getting hash using hash API")
        hash_url = (
            "{url}?username={username}&site={service}&password={password}".format(
                url=self.url,
                username=self.username,
                service=self.service.value,
                password=self.password,
            )
        )
        logger.debug("Fetching hash at {hash_url}".format(hash_url=hash_url))

        with urllib.request.urlopen(hash_url) as response:

            try:
                as_json = json.loads(response.read())

                if "hash" in as_json:
                    self.hash = as_json["hash"]
                    self.set_expiration_date(as_json["valid"])

            except Exception as e:
                logger.critical(e)

    def fetch_hash(self):
        now = datetime.now()

        if self.hash is None or now > self.expiration_date:
            logger.warning(
                "Hash is either none or may be expired. Getting a new one..."
            )

            if self.username is not None and self.password is not None:
                logger.debug("Username and password are not none.")

                try:
                    self._get_hash_via_hash_api()
                except urllib.error.HTTPError as error:
                    if error.code == 500:
                        self._get_hash_via_player()
                    else:
                        raise
                except Exception as e:
                    logger.critical(
                        "Could not fetch hash via hash API or modern player. Is SmoothStreams working?"
                    )
                    logger.critical(e)

            else:
                raise ValueError("Username or password is not set.")

        logger.debug("Got a hash!")
        return self.hash

    def set_expiration_date(self, minutes):
        now = datetime.now()
        self.expiration_date = now + timedelta(minutes=minutes - 1)
        logger.debug(
            "Expiration date set to {expiration_date}".format(
                expiration_date=self.expiration_date
            )
        )

    def _get_hash_via_player(self):
        logger.debug("Getting hash via modern player")
        # Set the API URL used by each site's modern player. I can only guarantee that
        # the one for Live247 works.
        if self.service == Service.LIVE247:
            api_url = (
                "https://live247.tv/fly/players/modern/api.php?action=regenerate&p=ipv4"
            )
        if self.service == Service.STARSTREAMS:
            api_url = (
                "https://starstreams.tv/players/modern/api.php?action=regenerate&p=ipv4"
            )
        if self.service == Service.STREAMTVNOW:
            api_url = (
                "https://streamtvnow.tv/players/modern/api.php?action=regenerate&p=ipv4"
            )

        # Set up the needed parameters to login to the above sites with. The sites are actually
        # WordPress so we need to login, grab the authorization cookie, then hit the URL again
        # to actually get the response we want.
        data = {
            "username": self.username,
            "password": self.password,
            "protect_login": "1",
        }
        data = urllib.parse.urlencode(data)
        data = data.encode("ascii")
        request = urllib.request.Request(url=api_url, data=data)

        # We need to set up an opener to reuse between requests as well as define a CookieJar
        # as by default urllib is stateless.
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        try:
            response = opener.open(request)

            if response.code == 200:
                response = opener.open(api_url)

                try:
                    as_json = json.loads(response.read())

                    self.hash = as_json["hash"]
                    self.set_expiration_date(as_json["expire"])

                except JSONDecodeError as e:
                    logger.critical(
                        "Could not load response as json! Possibly triggered CAPTCHA?"
                    )
                    raise e
                except Exception as e:
                    logger.critical(e)

        except Exception as e:
            logger.critical(e)
