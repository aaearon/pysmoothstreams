from unittest.mock import patch, MagicMock

from unittest import TestCase
from urllib.error import HTTPError
from pysmoothstreams.auth import AuthSign
from pysmoothstreams import Service
from pysmoothstreams.exceptions import InvalidService


class TestAuthSign(TestCase):
    def test_fetch_hash(self):
        with self.assertRaises(InvalidService) as context:
            AuthSign(service="ABC", auth=("fake", "password"))

        self.assertTrue("ABC is not a valid service!" in str(context.exception))

    @patch("urllib.request.urlopen")
    def test_fetch_hash_via_hash_api(self, mock_urlopen):
        hash_api_response = '{"hash":"c2VydmVyX3RpbWU9MTIvMTYvMjAyMCA0OjMxOjQ2IFBNJmhhc2hfdmFsdWU9WEkyeDYvd2F6UVFIRkpBTmpTamlqUT09JnZhbGlkbWludXRlcz0yNDAmaWQ9dmlldzI0Ny0xNDkx","valid":240,"code":"1"}'

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = hash_api_response
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        a.fetch_hash()

        self.assertEqual(
            "c2VydmVyX3RpbWU9MTIvMTYvMjAyMCA0OjMxOjQ2IFBNJmhhc2hfdmFsdWU9WEkyeDYvd2F6UVFIRkpBTmpTamlqUT09JnZhbGlkbWludXRlcz0yNDAmaWQ9dmlldzI0Ny0xNDkx",
            a.hash,
        )

    @patch("urllib.request.build_opener")
    @patch("urllib.request.urlopen")
    def test_fetch_hash_via_modern_player(self, mock_urlopen, mock_build_opener):
        hash_api_response = '{"hash":"c2VydmVyX3RpbWU9MTIvMTYvMjAyMCA0OjMxOjQ2IFBNJmhhc2hfdmFsdWU9WEkyeDYvd2F6UVFIRkpBTmpTamlqUT09JnZhbGlkbWludXRlcz0yNDAmaWQ9dmlldzI0Ny0xNDkx","expire":200}'

        # Mock so that the hash API returns a 500
        cm = MagicMock()
        cm.getcode.return_value = 500
        cm.read.return_value = None
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        mock_urlopen.side_effect = HTTPError(
            "https://auth.smoothstreams.tv/hash_api.php?username=fake&site=view247&password=fake",
            500,
            "Internal Error",
            {},
            None,
        )

        # Mock for the modern API.
        cm2 = MagicMock()
        cm2.code.return_value = 200
        cm2.open.return_value.code = 200
        cm2.open.return_value.read.return_value = hash_api_response
        cm2.__enter__.return_value = cm2
        mock_build_opener.return_value = cm2

        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        a.fetch_hash()

        self.assertEqual(
            "c2VydmVyX3RpbWU9MTIvMTYvMjAyMCA0OjMxOjQ2IFBNJmhhc2hfdmFsdWU9WEkyeDYvd2F6UVFIRkpBTmpTamlqUT09JnZhbGlkbWludXRlcz0yNDAmaWQ9dmlldzI0Ny0xNDkx",
            a.hash,
        )

    @patch("urllib.request.urlopen")
    def test_total_failure_when_fetching_hash(self, mock_urlopen):
        hash_api_response = '{"hash":"c2VydmVyX3RpbWU9MTIvMTYvMjAyMCA0OjMxOjQ2IFBNJmhhc2hfdmFsdWU9WEkyeDYvd2F6UVFIRkpBTmpTamlqUT09JnZhbGlkbWludXRlcz0yNDAmaWQ9dmlldzI0Ny0xNDkx","valid":200}'

        cm = MagicMock()
        cm.read.return_value = hash_api_response
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        mock_urlopen.side_effect = HTTPError(
            "https://auth.smoothstreams.tv/hash_api.php?username=fake&site=view247&password=fake",
            404,
            "Not Found",
            {},
            None,
        )

        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        with self.assertRaises(HTTPError):
            a.fetch_hash()
