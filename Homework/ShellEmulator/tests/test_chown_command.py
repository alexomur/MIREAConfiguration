import os
import unittest
import win32security
import pywintypes

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands.utils import resolve_path
from commands import Chown

class TestListCommand(unittest.TestCase):
    command: Command = Chown()

    def setUp(self):
        GlobalManager.set_current_path("/")

        zip_path = os.path.join(os.path.dirname(__file__), "test_archive.zip")
        global_zip_path = os.path.abspath(zip_path)
        extract_zip(global_zip_path)

        GlobalManager.set_exiting(False)

    def test_standard(self):
        self.assertEqual((True, "Successfully changed ownership of '/Test Folder 1/'"), self.command.execute(["Alexomur", "Test Folder 1"]))

        resolved = resolve_path("Test Folder 1")
        if not resolved:
            raise Exception("Error: File or directory '/Test Folder 1/' does not exist.")

    def test_not_enough_arguments(self):
        self.assertEqual((False, "Error: 'chown' requires at least two arguments.\nUsage:\n  chown <owner>[:<group>] <file>..."), self.command.execute([]))


if __name__ == '__main__':
    unittest.main()
