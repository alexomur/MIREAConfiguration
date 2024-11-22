import os
import unittest

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands import Cd

class TestListCommand(unittest.TestCase):
    command: Command = Cd()

    def setUp(self):
        GlobalManager.set_current_path("/")

        zip_path = os.path.join(os.path.dirname(__file__), "test_archive.zip")
        global_zip_path = os.path.abspath(zip_path)
        extract_zip(global_zip_path)

        GlobalManager.set_exiting(False)

    def test_standard(self):
        self.assertEqual((True, ""), self.command.execute(["Test Folder 1"]))

    def test_not_existing_file(self):
        self.assertEqual((False, "Error: Directory 'blah blah blah' does not exist."), self.command.execute(["blah blah blah"]))


if __name__ == '__main__':
    unittest.main()
