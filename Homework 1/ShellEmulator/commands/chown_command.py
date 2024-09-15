from .command_abc import Command
import win32security
import pywintypes
from win32security import (
    SetNamedSecurityInfo,
    SE_FILE_OBJECT,
    OWNER_SECURITY_INFORMATION,
    GROUP_SECURITY_INFORMATION,
)
from typing import List, Optional
from .utils import resolve_path
from typing import Tuple


class Chown(Command):
    name: str = "chown"
    aliases: List[str] = []
    description: str = "Changes the owner and/or group of a file or directory."

    def execute(self, arguments: List[str]) -> Tuple[bool, str]:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if len(arguments) < 2:
                return False, "Error: 'chown' requires at least two arguments.\nUsage:\n  chown <owner>[:<group>] <file>..."

            owner_group = arguments[0]
            files = arguments[1:]

            if ':' in owner_group:
                owner, group = owner_group.split(':', 1)
                group_sid = self.get_group_sid(group)
                if group_sid is None:
                    return False, ""
                security_info = OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION
            else:
                owner = owner_group
                group_sid = None  # Group not changed
                security_info = OWNER_SECURITY_INFORMATION

            owner_sid = self.get_user_sid(owner)
            if owner_sid is None:
                return False, f"Error: User '{owner}' does not exist."

            for file in files:
                resolved = resolve_path(file)
                if not resolved or resolved == (None, None):
                    return False, f"Error: File or directory '{file}' does not exist."

                virtual_path, real_path = resolved

                try:
                    SetNamedSecurityInfo(
                        real_path,
                        SE_FILE_OBJECT,
                        security_info,
                        owner_sid,
                        group_sid,
                        None,
                        None
                    )
                    return True, f"Successfully changed ownership of '{virtual_path}'"
                except pywintypes.error as e:
                    return True, f"Error changing ownership of '{virtual_path}': {e}"
                except Exception as e:
                    return True, f"Error changing ownership of '{virtual_path}': {e}"

        except Exception as e:
            return False, f"General error: {e}"

    @staticmethod
    def get_user_sid(username: str) -> Optional[pywintypes.SID]:
        try:
            user_handle = win32security.LookupAccountName(None, username)
            return user_handle[0]
        except win32security.error:
            return None

    @staticmethod
    def get_group_sid(groupname: str) -> Optional[pywintypes.SID]:
        try:
            group_handle = win32security.LookupAccountName(None, groupname)
            return group_handle[0]
        except win32security.error:
            print(f"Error: Group '{groupname}' does not exist.")
            return None
