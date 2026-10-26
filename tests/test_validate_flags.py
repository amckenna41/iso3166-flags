from scripts.validate_flags import *
import os
import shutil
import unittest
from PIL import Image
unittest.TestLoader.sortTestMethodsUsing = None

# @unittest.skip("Skipping tests.")
class Validate_Flags_Tests(unittest.TestCase):
    """
    Test suite for testing validate_flags.py script that checks the flag SVGs are safe
    to inline and the ISO 3166-2 flag filenames are valid subdivision codes.

    Test Cases
    ==========
    test_check_svg_safety:
        testing unsafe SVG content is reported and safe SVG content is not.
    test_check_iso3166_2_filenames:
        testing misnamed/misplaced ISO 3166-2 flags are reported and valid ones are not.
    test_check_svg_references:
        testing references to missing elements are reported and resolvable ones are not.
    test_check_file_format:
        testing a raster flag whose content doesn't match its extension is reported.
    """
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir_validate")
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        """ Delete the test output directory created in setUp. """
        shutil.rmtree(self.test_output_dir, ignore_errors=True)

    def write_svg(self, name: str, body: str) -> str:
        path = os.path.join(self.test_output_dir, name)
        with open(path, "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 4 3">{body}</svg>')
        return path

    # @unittest.skip("")
    def test_check_svg_safety(self):
        """ Testing unsafe SVG content is reported and safe SVG content is not. """
#1.)
        safe = self.write_svg("safe.svg", '<defs><path id="a" d="M0 0h4v3H0z"/></defs><use xlink:href="#a"/>'
                              '<image href="data:image/png;base64,AAAA"/><style>.x{fill:url(#a)}</style>')
        self.assertEqual(check_svg_safety(safe), [], "Expected local and data: references to be allowed.")
#2.)
        unsafe_bodies = {
            "script.svg": "<script>alert(1)</script>",
            "handler.svg": '<rect onload="alert(1)"/>',
            "js_href.svg": '<a href="javascript:alert(1)"><rect/></a>',
            "remote_href.svg": '<image xlink:href="https://example.com/x.png"/>',
            "remote_style.svg": "<style>@import url(//example.com/x.css);</style>",
            "remote_style_attr.svg": '<rect style="fill:url(https://example.com/x.svg#a)"/>',
        }
        for name, body in unsafe_bodies.items():
            self.assertTrue(check_svg_safety(self.write_svg(name, body)), f"Expected {name} to be reported as unsafe.")
#3.)
        broken = self.write_svg("broken.svg", "<rect>")
        self.assertTrue(check_svg_safety(broken), "Expected malformed XML to be reported.")

    # @unittest.skip("")
    def test_check_iso3166_2_filenames(self):
        """ Testing misnamed/misplaced ISO 3166-2 flags are reported and valid ones are not. """
        flag_dir = os.path.join(self.test_output_dir, "iso3166-2-flags")
        for path in ("GB/GB-ENG.svg", "GB/README.md", "GB/US-TX.svg", "GB/GB-XXX.svg", "GB/GB-SCT.gif", "ZZ/ZZ-01.svg", "loose.svg"):
            os.makedirs(os.path.join(flag_dir, os.path.dirname(path)), exist_ok=True)
            open(os.path.join(flag_dir, path), "w").close()

        errors = check_iso3166_2_filenames(flag_dir)
#1.)
        self.assertFalse(any("GB-ENG.svg" in e or "README.md" in e for e in errors), f"Expected valid flags and READMEs to pass: {errors}.")
#2.)
        for expected in ("US-TX.svg", "GB-XXX.svg", "GB-SCT.gif", "ZZ", "loose.svg"):
            self.assertTrue(any(expected in e for e in errors), f"Expected {expected} to be reported: {errors}.")

    # @unittest.skip("")
    def test_check_svg_references(self):
        """ Testing references to missing elements are reported and resolvable ones are not. """
#1.)
        valid = self.write_svg("valid_refs.svg", '<defs><linearGradient id="g"/><path id="p" d="M0 0h1v1z"/></defs>'
                               '<style>.a{fill:url(#g)}.unused{fill:url(#gone)}</style><use xlink:href="#p"/><rect class="a" fill="url(#g)"/>'
                               '<text style="shape-inside:url(#flowregion)">x</text>')
        self.assertEqual(check_svg_references(valid), [], "Expected resolvable references, unused CSS rules and shape-inside to pass.")
#2.)
        for name, body, ref in (("missing_use.svg", '<use xlink:href="#s"/>', "#s"),
                                ("missing_fill.svg", '<rect fill="url(#grad)"/>', "#grad"),
                                ("missing_class.svg", '<style>.st0{fill:url(#SVGID_1_)}</style><path class="st0"/>', "#SVGID_1_")):
            errors = check_svg_references(self.write_svg(name, body))
            self.assertTrue(any(ref in e for e in errors), f"Expected {name} to report missing {ref}: {errors}.")

    # @unittest.skip("")
    def test_check_file_format(self):
        """ Testing a raster flag whose content doesn't match its extension is reported. """
        png_path = os.path.join(self.test_output_dir, "real.png")
        webp_path = os.path.join(self.test_output_dir, "fake.png")
        Image.new("RGB", (4, 3), "red").save(png_path, "PNG")
        Image.new("RGB", (4, 3), "red").save(webp_path, "WEBP")
#1.)
        self.assertEqual(check_file_format(png_path), [], "Expected a real PNG to pass.")
#2.)
        self.assertTrue(check_file_format(webp_path), "Expected a WEBP saved as .png to be reported.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()
