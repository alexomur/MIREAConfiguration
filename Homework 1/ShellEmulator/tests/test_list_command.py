import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commands import list_command

class TestListCommand(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
