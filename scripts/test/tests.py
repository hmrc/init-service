import os
import sys

# dont do this in production code, this is bad practice it would seem, only for tests
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '../bin')

import unittest
from create import max_version_of

class TestActions(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple(self):
        self.assertTrue(True)

class MaxVersionTests(unittest.TestCase):

	def setUp(self):
		pass

	def testNaiveMaxVersion(self):
		self.assertEqual(max_version_of("0.1.0","0.2.0","0.3.0"), "0.3.0")

	def testNonalphabeticalMaxVersion(self):
		self.assertEqual(max_version_of("0.1.0","0.10.0","0.2.0"), "0.10.0")

	def testMaxVersionIgnoresNones(self):
		self.assertEqual(max_version_of("0.10.0",None), "0.10.0")

	def textMaxVersionWithMalformedSemVers(self):
		self.assertEqual(max_version_of("0.1.0","0.2"), "0.2")

	def testMaxVersionIgnoresText(self):
		self.assertEqual(max_version_of("0.10.0-SNAPSHOT","0.2.0"), "0.10.0-SNAPSHOT")

if __name__ == '__main__':
    unittest.main()
