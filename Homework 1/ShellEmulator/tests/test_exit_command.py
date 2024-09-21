import unittest

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands import Exit

class TestListCommand(unittest.TestCase):
    command: Command = Exit()

    def setUp(self):
        GlobalManager.set_current_path("/")
        GlobalManager.set_global_path(extract_zip("test_archive.zip"))
        GlobalManager.set_exiting(False)

    def test_standard(self):
        self.assertEqual((True, ""), self.command.execute([]))
        self.assertTrue(GlobalManager.exiting)

    def test_to_much_arguments(self):
        self.assertEqual((False, "Error: 'exit' command does not accept any arguments.\nUsage:\n  exit"), self.command.execute(["blah blah blah"]))


if __name__ == '__main__':
    unittest.main()
