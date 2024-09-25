import unittest
import os
import sys
import shutil
import tempfile
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualizer import main


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        shutil.copy(os.path.join(os.path.dirname(__file__), 'package-lock.json'), self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_generate_complete_tree(self):
        plantuml_content = """@startuml
[example-project]
[example-project] --> [dep1]
[dep1] --> [dep2]
[dep2] --> [dep3]
@enduml"""
        dependencies_path = 'dependencies.txt'
        with open(dependencies_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_content)
        max_depth = 3
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            main(dependencies_path, max_depth)
        output = f_capture.getvalue()
        expected_output = """└── example-project
    └── dep1
        └── dep2
            └── dep3
"""
        self.assertEqual(output, expected_output)

    def test_max_depth_limit(self):
        plantuml_content = """@startuml
[example-project]
[example-project] --> [dep1]
[dep1] --> [dep2]
[dep2] --> [dep3]
@enduml"""
        dependencies_path = 'dependencies.txt'
        with open(dependencies_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_content)
        max_depth = 1
        f_capture = io.StringIO()
        with redirect_stdout(f_capture):
            main(dependencies_path, max_depth)
        output = f_capture.getvalue()
        expected_output = """└── example-project
    └── dep1
"""
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
