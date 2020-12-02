import json
import logging
import urllib.request
from datetime import datetime, timedelta

from pysmoothstreams import Service
from pysmoothstreams.exceptions import InvalidService

logging = logging.getLogger(__name__)


class AuthSign:
    def __init__(self, service=Service.LIVE247, auth=(None, None)):
        self.service = self.__set_service(service)
        self.username = auth[0]
        self.password = auth[1]

        self.expiration_date = None
        self.hash = None

        self.url = "https://auth.smoothstreams.tv/hash_api.php"

        logging.debug(
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

    def fetch_hash(self):
        now = datetime.now()

        if self.hash is None or now > self.expiration_date:
            logging.warning(
                "Hash is either none or may be expired. Getting a new one..."
            )

            if self.username is not None and self.password is not None:
                logging.debug("Username and password are not none.")

                hash_url = "{url}?username={username}&site={service}&password={password}".format(
                    url=self.url,
                    username=self.username,
                    service=self.service.value,
                    password=self.password,
                )
                logging.debug("Fetching hash at {hash_url}".format(hash_url=hash_url))

                with urllib.request.urlopen(hash_url) as response:

                    try:
                        as_json = json.loads(response.read())

                        if "hash" in as_json:
                            self.hash = as_json["hash"]
                            self.set_expiration_date(as_json["valid"])

                    except Exception as e:
                        logging.critical(e)

            else:
                raise ValueError("Username or password is not set.")

        logging.debug(f"Got a hash!")
        return self.hash

    def set_expiration_date(self, minutes):
        now = datetime.now()
        self.expiration_date = now + timedelta(minutes=minutes - 1)
        logging.debug(
            "Expiration date set to {expiration_date}".format(
                expiration_date=self.expiration_date
            )
        )
