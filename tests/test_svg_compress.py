import os
import shutil
import subprocess
import tempfile
import unittest
import importlib.util

#scour can be invoked as a CLI or via its Python module - the script falls back to the module, so only the module is required
SCOUR_AVAILABLE = importlib.util.find_spec("scour") is not None

@unittest.skipUnless(SCOUR_AVAILABLE, "scour not installed")
class SVG_Compress_Tests(unittest.TestCase):
    """
    Test suite for the svg_compress.sh script that compresses SVG flags above a file size threshold.

    Test Cases
    ==========
    test_svg_compress_nested_folder:
        testing compressing a folder nested by country (iso3166-2-flags layout), mirroring sub-folders in the output.
    test_svg_compress_flat_folder:
        testing compressing a flat folder (iso3166-1-flags layout).
    """
    def setUp(self):
        """ Initialise test variables. """
        self.script = os.path.join("scripts", "svg_compress.sh")
        self.test_flag_folder = os.path.join("tests", "test_flags")
        self.temp_dir = tempfile.mkdtemp()

    def run_compress(self, input_folder: str, output_folder: str, filesize: int=1) -> subprocess.CompletedProcess:
        """ Run svg_compress.sh, returning the completed process. """
        return subprocess.run(["bash", self.script, f"--input={input_folder}", f"--output={output_folder}", f"--filesize={filesize}"],
                              capture_output=True, text=True, timeout=300)

    def test_svg_compress_nested_folder(self):
        """ Testing compressing a folder nested by country, mirroring the sub-folders in the output. """
        output = os.path.join(self.temp_dir, "nested")
        result = self.run_compress(self.test_flag_folder, output)
#1.)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("files successfully compressed and copied", result.stdout)
#2.)
        #every input flag has a counterpart at the same relative path, SVGs over the threshold no larger than the original
        for country in ("FI", "SB"):
            for f in os.listdir(os.path.join(self.test_flag_folder, country)):
                if f == "README.md":
                    continue
                src, dst = os.path.join(self.test_flag_folder, country, f), os.path.join(output, country, f)
                self.assertTrue(os.path.isfile(dst), f"Expected {dst} in the output folder.")
                if f.endswith(".svg"):
                    self.assertLessEqual(os.path.getsize(dst), os.path.getsize(src), f"Expected {f} not to grow when compressed.")
        self.assertFalse(os.path.isfile(os.path.join(output, "FI", "README.md")), "Expected README files to be skipped.")

    def test_svg_compress_flat_folder(self):
        """ Testing compressing a flat folder of flags, as in iso3166-1-flags. """
        flat_input = os.path.join(self.temp_dir, "flat_input")
        os.makedirs(flat_input)
        for f in ("FI-01.svg", "FI-02.svg", "FI-03.svg"):
            shutil.copy(os.path.join(self.test_flag_folder, "FI", f), flat_input)
        output = os.path.join(self.temp_dir, "flat_output")
        result = self.run_compress(flat_input, output)
#1.)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(sorted(os.listdir(output)), ["FI-01.svg", "FI-02.svg", "FI-03.svg"], "Expected flat output mirroring the flat input.")

    def tearDown(self):
        """ Delete the temp folders. """
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    #run all unit tests
    unittest.main()
