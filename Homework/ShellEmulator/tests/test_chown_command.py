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

    @staticmethod
    def get_owner(path: str) -> str:
        try:
            security_info = win32security.OWNER_SECURITY_INFORMATION
            security_descriptor = win32security.GetFileSecurity(path, security_info)
            owner_sid = security_descriptor.GetSecurityDescriptorOwner()

            name, domain, type = win32security.LookupAccountSid(None, owner_sid)
            return f"{domain}\\{name}"
        except pywintypes.error as e:
            return f"Error retrieving owner for '{path}': {e.strerror} (Code: {e.winerror})"
        except Exception as e:
            return f"General error: {str(e)}"

    def setUp(self):
        GlobalManager.set_current_path("/")

        zip_path = os.path.join(os.path.dirname(__file__), "test_archive.zip")
        global_zip_path = os.path.abspath(zip_path)
        GlobalManager.set_global_path(extract_zip(global_zip_path))

        GlobalManager.set_exiting(False)

    def test_standard(self):
        new_owner: str = "Alexomur"
        self.assertEqual((True, "Successfully changed ownership of '/Test Folder 1'"), self.command.execute([new_owner, "Test Folder 1"]))

        resolved = resolve_path("Test Folder 1")
        if not resolved or resolved == (None, None):
            raise Exception("Error: File or directory 'Test Folder 1' does not exist.")
        _, real_path = resolved

        self.assertIn(new_owner.lower(), str(real_path).lower())

    def test_not_enough_arguments(self):
        self.assertEqual((False, "Error: 'chown' requires at least two arguments.\nUsage:\n  chown <owner>[:<group>] <file>..."), self.command.execute([]))


if __name__ == '__main__':
    unittest.main()
