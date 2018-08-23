from unittest import TestCase

from pysmoothstreams.auth import AuthSign


class TestAuthSign(TestCase):
	def test_fetch_hash(self):
		with self.assertRaises(TypeError) as context:
			AuthSign(service='ABC', auth=('fake', 'password'))

		self.assertTrue('ABC is not a valid service!' in str(context.exception))
