from .command_abc import Command
import os
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


class Chown(Command):
    name: str = "chown"
    aliases: List[str] = []
    description: str = "Changes the owner and/or group of a file or directory."

    def execute(self, arguments: List[str]) -> bool:
        """
        :param arguments: List of command-line arguments.
        :return: True if executed successfully, False otherwise.
        """
        try:
            if len(arguments) < 2:
                print("Error: 'chown' requires at least two arguments.")
                print("Usage:")
                print("  chown <owner>[:<group>] <file>...")
                return False

            owner_group = arguments[0]
            files = arguments[1:]

            if ':' in owner_group:
                owner, group = owner_group.split(':', 1)
                group_sid = self.get_group_sid(group)
                if group_sid is None:
                    return False
                security_info = OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION
            else:
                owner = owner_group
                group_sid = None  # Group not changed
                security_info = OWNER_SECURITY_INFORMATION

            owner_sid = self.get_user_sid(owner)
            if owner_sid is None:
                print(f"Error: User '{owner}' does not exist.")
                return False

            for file in files:
                resolved = resolve_path(file)
                if not resolved or resolved == (None, None):
                    print(f"Error: File or directory '{file}' does not exist.")
                    continue

                virtual_path, real_path = resolved

                try:
                    # Устанавливаем владельца и/или группу с помощью SetNamedSecurityInfo
                    SetNamedSecurityInfo(
                        real_path,
                        SE_FILE_OBJECT,
                        security_info,
                        owner_sid,
                        group_sid,
                        None,
                        None
                    )
                    print(f"Successfully changed ownership of '{virtual_path}'")
                except pywintypes.error as e:
                    print(f"Error changing ownership of '{virtual_path}': {e}")
                except Exception as e:
                    print(f"Error changing ownership of '{virtual_path}': {e}")

            return True

        except Exception as e:
            print(f"General error: {e}")
            return False

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
