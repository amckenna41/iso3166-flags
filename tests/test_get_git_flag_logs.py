from scripts.get_git_flag_logs import *
import scripts.get_git_flag_logs as get_git_flag_logs_module
import os
import csv
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Get_Git_Flag_Logs_Tests(unittest.TestCase):
    """
    Test suite for testing get_git_flag_logs.py script that exports the git status
    change log for the flag folders.

    Test Cases
    ==========
    test_get_git_timestamp_status:
        testing the status parameter is respected when a file has no git commit history.
    test_extract_file_metadata:
        testing the folder/filename/extension are correctly parsed from a file path.
    test_export_git_flag_logs_status_forwarded:
        testing the parsed 'git status' status is forwarded through to the timestamp lookup (regression test).
    """
    def setUp(self):
        """ Initialise test variables. """
        #a path that is guaranteed to have no git commit history
        self.test_uncommitted_path = "this/path/does/not/exist/in/git/history.svg"
        self.test_output_dir = os.path.join("tests", "test_output_dir")

        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

    # @unittest.skip("")
    def test_get_git_timestamp_status(self):
        """ Testing the status parameter is respected when a file has no git commit history. """
#1.)
        #a "modified"/"deleted" file with no commit history should report as not-committed
        modified_timestamp = get_git_timestamp(self.test_uncommitted_path, "modified")
        self.assertEqual(modified_timestamp, "not-committed", "Expected a modified file with no commit history to be reported as not-committed.")
#2.)
        deleted_timestamp = get_git_timestamp(self.test_uncommitted_path, "deleted")
        self.assertEqual(deleted_timestamp, "not-committed", "Expected a deleted file with no commit history to be reported as not-committed.")
#3.)
        #an "added" file with no commit history falls back to a filesystem timestamp, empty if the file doesn't exist on disk either
        added_timestamp = get_git_timestamp(self.test_uncommitted_path, "added")
        self.assertEqual(added_timestamp, "", "Expected an added, non-existent file to fall back to an empty filesystem timestamp.")

    # @unittest.skip("")
    def test_extract_file_metadata(self):
        """ Testing the folder/filename/extension are correctly parsed from a file path. """
#1.)
        folder, filename, extension = extract_file_metadata(os.path.join("iso3166-1-flags", "ad.svg"))
        self.assertEqual(folder, "iso3166-1-flags", "Expected folder to be parsed from the file path.")
        self.assertEqual(filename, "ad.svg", "Expected filename to be parsed from the file path.")
        self.assertEqual(extension, "SVG", "Expected extension to be uppercased.")
#2.)
        with self.assertRaises(OSError):
            extract_file_metadata("invalid_filepath.svg")

    # @unittest.skip("")
    def test_export_git_flag_logs_status_forwarded(self):
        """ Testing the parsed 'git status' status is forwarded through to the timestamp lookup (regression test). """
        #an untracked-on-disk file so "git log" genuinely finds no commit history for it, mirroring a
        #file that shows as "modified" in git status but has never actually been committed
        test_file = os.path.join(self.test_output_dir, "untracked_test_flag.svg")
        with open(test_file, "w") as f:
            f.write("<svg></svg>")

        #fake "git status" output reporting the test file as modified, real "git log"/"git diff" calls still run
        def fake_run(cmd, *args, **kwargs):
            class FakeResult:
                pass
            result = FakeResult()
            if cmd[:2] == ["git", "status"]:
                result.stdout = f"Changes not staged for commit:\n\tmodified:   {test_file}\n"
            else:
                result.stdout = ""
            return result

        export_output = os.path.join(self.test_output_dir, "test_git_status_logs.csv")
        original_run = get_git_flag_logs_module.subprocess.run
        get_git_flag_logs_module.subprocess.run = fake_run
        try:
            export_git_flag_logs(export_filename=export_output, folders_to_check=self.test_output_dir, include_timestamp=True)
        finally:
            get_git_flag_logs_module.subprocess.run = original_run
            os.remove(test_file)

        with open(export_output, newline="") as f:
            rows = list(csv.DictReader(f))
#1.)
        self.assertEqual(len(rows), 1, "Expected exactly one row for the fake modified file.")
        self.assertEqual(rows[0]["timestamp"], "not-committed",
            "Expected a modified file with no git commit history to be logged as not-committed, confirming the status is forwarded to the timestamp lookup.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()
