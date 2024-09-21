import unittest

from zip_handler import extract_zip

from commands import Command, GlobalManager
from commands import History

class TestListCommand(unittest.TestCase):
    command: Command = History()

    def setUp(self):
        GlobalManager.set_current_path("/")
        GlobalManager.set_global_path(extract_zip("test_archive.zip"))
        GlobalManager.set_exiting(False)

        GlobalManager.clear_command_history()
        GlobalManager.add_command_history("cd 'Test Folder 1' | True")
        GlobalManager.add_command_history("ls | True")
        GlobalManager.add_command_history("cd .. | True")
        GlobalManager.add_command_history("cd | False")

    def test_standard(self):
        self.assertEqual((True, "1  cd 'Test Folder 1' | True\n2  ls | True\n3  cd .. | True\n4  cd | False\n"), self.command.execute([]))

    def test_to_much_arguments(self):
        self.assertEqual((False, "Error: Invalid argument 'blah blah blah' for 'history'.\nUsage:\n  history [N]"), self.command.execute(["blah blah blah"]))


if __name__ == '__main__':
    unittest.main()
