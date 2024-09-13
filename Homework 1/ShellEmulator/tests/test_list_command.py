import unittest
from commands.list_command import List
from unittest.mock import patch, MagicMock
import __main__ as main

class TestListCommand(unittest.TestCase):
    def setUp(self):
        self.list_command = List()

    @patch('commands.list_command.resolve_path')
    @patch('os.listdir')
    def test_execute_no_arguments_success(self, mock_listdir, mock_resolve_path):
        # Устанавливаем текущий путь
        main.current_path = '/virtual/path'
        virtual_directory = '/virtual/path'
        real_directory = '/real/path'
        mock_resolve_path.return_value = (virtual_directory, real_directory)
        mock_listdir.return_value = ['file1.txt', 'file2.txt']

        with patch('builtins.print') as mock_print:
            result = self.list_command.execute([])

        mock_resolve_path.assert_called_with(main.current_path)
        mock_listdir.assert_called_with(real_directory)
        self.assertTrue(result)
        mock_print.assert_any_call('file1.txt')
        mock_print.assert_any_call('file2.txt')

    @patch('commands.list_command.resolve_path')
    def test_execute_directory_not_exist(self, mock_resolve_path):
        main.current_path = '/virtual/path'
        virtual_directory = '/virtual/path'
        real_directory = None
        mock_resolve_path.return_value = (virtual_directory, real_directory)

        with patch('builtins.print') as mock_print:
            result = self.list_command.execute([])

        mock_resolve_path.assert_called_with(main.current_path)
        mock_print.assert_called_with(f"Error: Directory '{virtual_directory}' does not exist.")
        self.assertFalse(result)

    @patch('commands.list_command.resolve_path')
    @patch('os.listdir')
    def test_execute_permission_error(self, mock_listdir, mock_resolve_path):
        main.current_path = '/virtual/path'
        virtual_directory = '/virtual/path'
        real_directory = '/real/path'
        mock_resolve_path.return_value = (virtual_directory, real_directory)
        mock_listdir.side_effect = PermissionError

        with patch('builtins.print') as mock_print:
            result = self.list_command.execute([])

        mock_resolve_path.assert_called_with(main.current_path)
        mock_listdir.assert_called_with(real_directory)
        mock_print.assert_called_with(f"Error: Permission denied for directory '{virtual_directory}'.")
        self.assertFalse(result)

    @patch('commands.list_command.resolve_path')
    @patch('os.listdir')
    def test_execute_general_exception(self, mock_listdir, mock_resolve_path):
        main.current_path = '/virtual/path'
        virtual_directory = '/virtual/path'
        real_directory = '/real/path'
        mock_resolve_path.return_value = (virtual_directory, real_directory)
        mock_listdir.side_effect = Exception('Test exception')

        with patch('builtins.print') as mock_print:
            result = self.list_command.execute([])

        mock_resolve_path.assert_called_with(main.current_path)
        mock_listdir.assert_called_with(real_directory)
        mock_print.assert_called_with(f"Error accessing directory '{virtual_directory}': Test exception")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
