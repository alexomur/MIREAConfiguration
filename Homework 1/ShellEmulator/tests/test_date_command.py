import unittest
from datetime import datetime

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands import Date

class TestListCommand(unittest.TestCase):
    command: Command = Date()

    def setUp(self):
        GlobalManager.set_current_path("/")
        GlobalManager.set_global_path(extract_zip("test_archive.zip"))
        GlobalManager.set_exiting(False)

    def test_standard(self):
        self.assertEqual((True, datetime.now().strftime("%a %b %d %H:%M:%S %Y")), self.command.execute([]))

    def test_to_much_arguments(self):
        self.assertEqual((False, "Error: Format must start with '+'. For example, '+%Y-%m-%d %H:%M:%S'."), self.command.execute(["blah blah blah"]))


if __name__ == '__main__':
    unittest.main()
