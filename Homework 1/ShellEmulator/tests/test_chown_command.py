import unittest

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands import Chown

class TestListCommand(unittest.TestCase):
    command: Command = Chown()

    def setUp(self):
        GlobalManager.set_current_path("/")
        GlobalManager.set_global_path(extract_zip("test_archive.zip"))
        GlobalManager.set_exiting(False)

    def test_standard(self):
        self.assertEqual((True, "Successfully changed ownership of '/Test Folder 1'"), self.command.execute(["alexomur", "Test Folder 1"]))

    def test_not_enough_arguments(self):
        self.assertEqual((False, "Error: 'chown' requires at least two arguments.\nUsage:\n  chown <owner>[:<group>] <file>..."), self.command.execute([]))


if __name__ == '__main__':
    unittest.main()
