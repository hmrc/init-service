import os
import sys

# dont do this in production code, this is bad practice it would seem, only for tests
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '../bin')

import unittest

class TestActions(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
