import unittest
import os
import sys
import shutil
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main


class TestPlantUMLGeneration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        shutil.copy(os.path.join(os.path.dirname(__file__), 'package-lock.json'), self.test_dir)
        with open('visualizer.py', 'w', encoding='utf-8') as f:
            f.write("# Фиктивный визуализатор")

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_generate_plantuml_file(self):
        lockfile_path = 'package-lock.json'
        plantuml_path = 'visualizer.py'
        max_depth = 2
        main.main(lockfile_path, plantuml_path, max_depth)
        self.assertTrue(os.path.exists('dependencies.txt'))
        with open('dependencies.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertTrue(content.startswith('@startuml'))
        self.assertTrue(content.strip().endswith('@enduml'))
        self.assertIn('[example-project]', content)
        self.assertIn('[example-project] --> [dep1]', content)

    def test_max_depth_limit(self):
        lockfile_path = 'package-lock.json'
        plantuml_path = 'visualizer.py'
        max_depth = 1
        main.main(lockfile_path, plantuml_path, max_depth)
        self.assertTrue(os.path.exists('dependencies.txt'))
        with open('dependencies.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('[example-project]', content)
        self.assertIn('[example-project] --> [dep1]', content)
        self.assertNotIn('[dep1] --> [dep2]', content)


if __name__ == '__main__':
    unittest.main()
