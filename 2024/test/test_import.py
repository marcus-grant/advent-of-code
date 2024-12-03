# test/test_import.py
import unittest
import sys
import os
from unittest.mock import patch

# Adjust sys.path to include the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import dynamic_import after adjusting sys.path
try:
    from util.sols import dynamic_import
except ModuleNotFoundError as e:
    print(f"❌ Failed to import dynamic_import: {e}")
    dynamic_import = None


class TestDynamicImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Check if dynamic_import was successfully imported.
        """
        if dynamic_import is None:
            raise unittest.SkipTest("dynamic_import function is not available.")

    def setUp(self):
        """
        Patch 'cprint' and 'console.print' to suppress output during tests.
        """
        # Patch 'util.sols.cprint'
        self.patcher_cprint = patch("util.sols.cprint")
        self.mock_cprint = self.patcher_cprint.start()

        # Patch 'util.sols.console.print'
        self.patcher_console_print = patch("util.sols.console.print")
        self.mock_console_print = self.patcher_console_print.start()

    def tearDown(self):
        """
        Stop patching after each test method.
        """
        self.patcher_cprint.stop()
        self.patcher_console_print.stop()

    def test_import_existing_days(self):
        """
        Test importing existing days (01-03). Each should import successfully
        and have part1 and part2 functions.
        """
        existing_days = [f"{i:02d}" for i in range(1, 4)]  # Test days 01 to 03
        for day in existing_days:
            with self.subTest(day=day):
                module = dynamic_import(day)  # type: ignore
                msg_notnone = f"Failed to import Day {day}/solve.py"
                msg_p1 = f"Missing 'part1' in Day {day}/solve.py"
                msg_p2 = f"Missing 'part2' in Day {day}/solve.py"
                self.assertIsNotNone(module, msg_notnone)
                self.assertTrue(hasattr(module, "part1"), msg_p1)
                self.assertTrue(hasattr(module, "part2"), msg_p2)

    def test_import_non_existing_days(self):
        """
        Test importing non-existing days (26, 99). Each should fail to import
        and return None.
        """
        non_existing_days = [f"{i:02d}" for i in [26, 99]]
        for day in non_existing_days:
            with self.subTest(day=day):
                module = dynamic_import(day)  # type: ignore
                msg = f"Imported Day {day}/solve.py which should not exist"
                self.assertIsNone(module, msg)


if __name__ == "__main__":
    unittest.main()
