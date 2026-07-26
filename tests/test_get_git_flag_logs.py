from scripts.get_git_flag_logs import *
import scripts.get_git_flag_logs as get_git_flag_logs_module
import os
import csv
import shutil
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
    test_parse_porcelain_status:
        testing the machine-readable git status output is parsed into (status, path) tuples.
    test_export_git_flag_logs_deleted_file:
        testing a deleted flag is logged rather than raising an error (regression test).
    """
    def setUp(self):
        """ Initialise test variables. """
        #a path that is guaranteed to have no git commit history
        self.test_uncommitted_path = "this/path/does/not/exist/in/git/history.svg"
        self.test_output_dir = os.path.join("tests", "test_output_dir")

        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

    def tearDown(self):
        """ Delete the test output directory created in setUp. """
        if (os.path.isdir(self.test_output_dir)):
            shutil.rmtree(self.test_output_dir)

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
        #paths are parsed as strings and don't need to exist on disk - deleted flags are reported
        #by git status precisely because they've been removed (regression test)
        folder, filename, extension = extract_file_metadata(os.path.join("iso3166-1-flags", "deleted_flag.svg"))
        self.assertEqual(folder, "iso3166-1-flags", "Expected a deleted file's folder to still be parsed.")
        self.assertEqual(filename, "deleted_flag.svg", "Expected a deleted file's filename to still be parsed.")
        self.assertEqual(extension, "SVG", "Expected a deleted file's extension to still be parsed.")
#3.)
        #a bare filename has no parent folder to parse
        folder, filename, extension = extract_file_metadata("invalid_filepath.svg")
        self.assertEqual(folder, "", "Expected an empty folder for a path with no parent directory.")
        self.assertEqual(filename, "invalid_filepath.svg", "Expected the filename to be parsed from a bare path.")

    # @unittest.skip("")
    def test_export_git_flag_logs_status_forwarded(self):
        """ Testing the parsed 'git status' status is forwarded through to the timestamp lookup (regression test). """
        #an untracked-on-disk file so "git log" genuinely finds no commit history for it, mirroring a
        #file that shows as "modified" in git status but has never actually been committed
        test_file = os.path.join(self.test_output_dir, "untracked_test_flag.svg")
        with open(test_file, "w") as f:
            f.write("<svg></svg>")

        #fake "git status" porcelain output reporting the test file as modified in the worktree,
        #real "git log"/"git diff" calls still run
        def fake_run(cmd, *args, **kwargs):
            class FakeResult:
                pass
            result = FakeResult()
            if cmd[:2] == ["git", "status"]:
                result.stdout = f" M {test_file}\0"
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

    # @unittest.skip("")
    def test_parse_porcelain_status(self):
        """ Testing the machine-readable git status output is parsed into (status, path) tuples. """
#1.)
        #staged add, staged modify, unstaged modify, deleted, untracked and a path containing a space
        porcelain = "\0".join([
            "A  iso3166-1-flags/aa.svg",
            "M  iso3166-1-flags/bb.svg",
            " M iso3166-1-flags/cc.svg",
            " D iso3166-1-flags/dd.svg",
            "?? iso3166-1-flags/ee.svg",
            "?? iso3166-2-flags/GB/GB ABC.svg",
        ]) + "\0"

        self.assertEqual(parse_porcelain_status(porcelain), [
            ("added", "iso3166-1-flags/aa.svg"),
            ("modified", "iso3166-1-flags/bb.svg"),
            ("modified", "iso3166-1-flags/cc.svg"),
            ("deleted", "iso3166-1-flags/dd.svg"),
            ("added", "iso3166-1-flags/ee.svg"),
            ("added", "iso3166-2-flags/GB/GB ABC.svg"),
        ], "Expected staged, unstaged, deleted and untracked entries to all be parsed, including paths with spaces.")
#2.)
        #renames are followed by a second NUL-terminated token holding the original path, which is skipped
        renamed = "R  iso3166-1-flags/new.svg\0iso3166-1-flags/old.svg\0 M iso3166-1-flags/other.svg\0"
        self.assertEqual(parse_porcelain_status(renamed), [
            ("modified", "iso3166-1-flags/new.svg"),
            ("modified", "iso3166-1-flags/other.svg"),
        ], "Expected the original path of a rename to be skipped without shifting the following entry.")
#3.)
        #ignored and unmerged entries are not change-log entries
        self.assertEqual(parse_porcelain_status("!! iso3166-1-flags/ignored.svg\0UU iso3166-1-flags/conflict.svg\0"), [],
            "Expected ignored and unmerged entries to be excluded.")
#4.)
        self.assertEqual(parse_porcelain_status(""), [], "Expected empty git status output to produce no changes.")

    # @unittest.skip("")
    def test_export_git_flag_logs_deleted_file(self):
        """ Testing a deleted flag is logged rather than raising an error (regression test). """
        #a deleted file no longer exists on disk, which previously raised an OSError mid-export
        deleted_file = os.path.join(self.test_output_dir, "deleted_test_flag.svg")

        def fake_run(cmd, *args, **kwargs):
            class FakeResult:
                pass
            result = FakeResult()
            result.stdout = f" D {deleted_file}\0" if cmd[:2] == ["git", "status"] else ""
            return result

        export_output = os.path.join(self.test_output_dir, "test_git_status_logs_deleted.csv")
        original_run = get_git_flag_logs_module.subprocess.run
        get_git_flag_logs_module.subprocess.run = fake_run
        try:
            export_git_flag_logs(export_filename=export_output, folders_to_check=self.test_output_dir, include_timestamp=True)
        finally:
            get_git_flag_logs_module.subprocess.run = original_run

        with open(export_output, newline="") as f:
            rows = list(csv.DictReader(f))
#1.)
        self.assertEqual(len(rows), 1, "Expected the deleted file to be exported rather than raising an error.")
        self.assertEqual(rows[0]["status"], "deleted", "Expected the deleted file's status to be logged as deleted.")
        self.assertEqual(rows[0]["filename"], "deleted_test_flag.svg", "Expected the deleted file's name to be parsed from its path.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()
