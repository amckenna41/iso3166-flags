from scripts.generate_css import *
import shutil
import os
from iso3166_2 import Subdivisions
import iso3166
import re
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Generate_CSS_Tests(unittest.TestCase):
    """
    Test suite for testing generate_css.py script that exports the CSS files
    for the ISO 3166-1 & ISO 3166-2 flags.

    Test Cases
    ==========
    test_create_iso3166_1_css:
        testing functionality that generates the ISO 3166-1 CSS file.
    test_create_iso3166_2_css:
        testing functionality that generates the ISO 3166-2 CSS file.
    test_css_selector_uniqueness:
        testing CSS selector uniqueness (no duplicates).
    test_css_syntax_validity:
        testing CSS syntax is valid.
    test_css_file_size_limits:
        testing CSS file size limits.
    test_background_image_urls:
        testing background-image URLs are correct/accessible.
    test_empty_directory_handling:
        testing handling of empty directories.
    test_create_iso3166_2_svg_sprite_global:
        testing generating a single global ISO 3166-2 SVG sprite file.
    test_create_iso3166_2_svg_sprite_per_country:
        testing generating one smaller ISO 3166-2 SVG sprite file per country.
    test_create_iso3166_3_css:
        testing generating the ISO 3166-3 (former country) CSS file.
    test_css_dir_relative_urls:
        testing flag url() paths are relative to the css_dir the CSS is served from.
    test_create_svg_sprite:
        testing generating the ISO 3166-1 SVG sprite file.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_iso3166_1_flag_folder = "iso3166-1-flags"
        self.test_iso3166_2_flag_folder = "iso3166-2-flags"
        self.test_empty_folder = os.path.join(self.test_output_dir, "empty_folder")
        self.subdivisions = Subdivisions()
        self.max_css_file_size_mb = 5  # 5MB max CSS file size

        #create test directory if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)
        
        #create empty test folder
        if not (os.path.isdir(self.test_empty_folder)):
            os.makedirs(self.test_empty_folder)

    # @unittest.skip("")
    def test_create_iso3166_1_css(self):
        """ Testing the function that generates the ISO 3166-1 CSS file. """
#1.)
        create_iso3166_1_css(self.test_iso3166_1_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-1.css"))

        #open generated CSS file
        with open(os.path.join(self.test_output_dir, "test-iso3166-1.css"), encoding="utf-8") as f:
            test_css_content = f.read()
        
        #get list of country code & those selector exception codes
        all_country_codes = list(iso3166.countries_by_alpha2.keys())
        country_code_exceptions = ["gb-nir", "gb-sct", "gb-wls", "gb-eng", "ac", "ta", "cp", "cq", "dg", "ea", "ez", "fx", "ic", "su", "uk", "xk", "xx", "un", "eu", "pc"]

        #get regex pattern to match the required selectors
        selector_pattern = re.compile(r'\.fi-([a-z]{2})\s*\{[^}]*?background-image:', re.IGNORECASE)
        matches = selector_pattern.findall(test_css_content)

        #iterate over all selectors, validating the country code are valid
        for code in matches:
            normalized = code.upper()
            if (normalized.lower() in country_code_exceptions): #skip exception selectors
                continue
            if normalized not in all_country_codes:
                self.fail(f"Unexpected country code selector found: {normalized}.")

    # @unittest.skip("")
    def test_create_iso3166_2_css(self):
        """ Testing the function that generates the ISO 3166-2 CSS file. """
        all_subdivision_codes = self.subdivisions.subdivision_codes()
#1.)    
        create_iso3166_2_css(self.test_iso3166_2_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-2.css"))

        #open generated CSS file
        with open(os.path.join(self.test_output_dir, "test-iso3166-2.css"), encoding="utf-8") as f:
            test_css_content = f.read()

        #get regex pattern to match the required selectors
        selector_pattern = re.compile(r'\.fi-([a-z]{2})-\1-([a-z0-9\-]+)', re.IGNORECASE)
        matches = selector_pattern.findall(test_css_content)

        #iterate over all selectors, validating the country code and subdivision codes are valid
        for country_code, subd_code in matches:
            normalized_country = country_code.upper()
            normalized_subdivision = f"{normalized_country}-{subd_code.upper()}"

            if normalized_country not in all_subdivision_codes:
                self.fail(f"Unexpected country code in selector: {normalized_country}.")

            if normalized_subdivision not in all_subdivision_codes[normalized_country]:
                self.fail(f"Unexpected subdivision code in selector: {normalized_subdivision}.")

    # @unittest.skip("")
    def test_css_selector_uniqueness(self):
        """ Testing CSS selector uniqueness (no duplicates). """
        create_iso3166_1_css(self.test_iso3166_1_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-1.css"))
        
        with open(os.path.join(self.test_output_dir, "test-iso3166-1.css"), encoding="utf-8") as f:
            test_css_content = f.read()
        
        #extract all selectors
        selector_pattern = re.compile(r'\.fi-([a-z0-9\-]+)\s*\{', re.IGNORECASE)
        selectors = selector_pattern.findall(test_css_content)
        
        #check for duplicates
        seen = set()
        duplicates = []
        for selector in selectors:
            if selector in seen:
                duplicates.append(selector)
            seen.add(selector)
#1.)        
        self.assertEqual(len(duplicates), 0, f"Found duplicate CSS selectors: {duplicates}")

    # @unittest.skip("")
    def test_css_syntax_validity(self):
        """ Testing CSS syntax is valid. """
        create_iso3166_1_css(self.test_iso3166_1_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-1.css"))
        
        with open(os.path.join(self.test_output_dir, "test-iso3166-1.css"), encoding="utf-8") as f:
            test_css_content = f.read()
        
        #basic CSS syntax validation
        open_braces = test_css_content.count('{')
        close_braces = test_css_content.count('}')
#1.)        
        self.assertEqual(open_braces, close_braces, "CSS has mismatched braces.")
        
        #check for required CSS properties
        self.assertIn("background-image", test_css_content, "CSS should contain background-image property.")
        self.assertIn("background-size", test_css_content, "CSS should contain background-size property.")
        
        #validate each rule has proper structure
        rule_pattern = re.compile(r'\.fi-[a-z0-9\-]+\s*\{[^}]+\}', re.IGNORECASE)
        rules = rule_pattern.findall(test_css_content)
        self.assertGreater(len(rules), 0, "CSS should contain valid rules.")

    # @unittest.skip("")
    def test_css_file_size_limits(self):
        """ Testing CSS file size limits. """
        create_iso3166_2_css(self.test_iso3166_2_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-2.css"))
        
        css_file_path = os.path.join(self.test_output_dir, "test-iso3166-2.css")
        file_size_mb = os.path.getsize(css_file_path) / (1024 * 1024)
#1.)        
        self.assertLess(file_size_mb, self.max_css_file_size_mb, 
                       f"CSS file size ({file_size_mb:.2f}MB) exceeds maximum ({self.max_css_file_size_mb}MB).")

    # @unittest.skip("")
    def test_background_image_urls(self):
        """ Testing background-image URLs are correct/accessible. """
        create_iso3166_1_css(self.test_iso3166_1_flag_folder, export_css_filepath=os.path.join(self.test_output_dir, "test-iso3166-1.css"))
        
        with open(os.path.join(self.test_output_dir, "test-iso3166-1.css"), encoding="utf-8") as f:
            test_css_content = f.read()
        
        #extract all background-image URLs
        url_pattern = re.compile(r'background-image:\s*url\(([^)]+)\)', re.IGNORECASE)
        urls = url_pattern.findall(test_css_content)
#1.)        
        self.assertGreater(len(urls), 0, "CSS should contain background-image URLs.")
        
        #CSS url() paths resolve relative to the stylesheet, so every URL must point at a real file from the CSS file's directory
        for url in urls:
            url = url.strip('\'"')
            file_path = os.path.join(self.test_output_dir, url)
            self.assertTrue(os.path.isfile(file_path), f"Background-image URL does not resolve relative to the stylesheet: {url}")

        #without the ::before content the empty <span> collapses to 0px high and no flag renders
        self.assertIn('.fi::before {\n\tcontent: "\\00a0";\n}', test_css_content, "Expected .fi::before rule giving flag spans a height.")

    # @unittest.skip("")
    def test_empty_directory_handling(self):
        """ Testing handling of empty directories. """
        empty_css_path = os.path.join(self.test_output_dir, "empty-test.css")
        
        #create CSS from empty folder - should create file with base styles only
        create_iso3166_1_css(self.test_empty_folder, export_css_filepath=empty_css_path)
#1.)        
        self.assertTrue(os.path.isfile(empty_css_path), "CSS file should be created even for empty directory.")
        
        with open(empty_css_path, encoding="utf-8") as f:
            content = f.read()
        
        #should contain base styles but no flag-specific selectors
        self.assertIn(".fib", content, "Should contain base .fib class.")
        self.assertIn(".fi", content, "Should contain base .fi class.")

    # @unittest.skip("")
    def test_create_iso3166_2_svg_sprite_global(self):
        """ Testing generating a single global ISO 3166-2 SVG sprite file. """
        sprite_path = os.path.join(self.test_output_dir, "iso3166-2-sprite.svg")
#1.)
        create_iso3166_2_svg_sprite(country_input_folder=os.path.join("tests", "test_flags"), export_sprite_filepath=sprite_path)

        self.assertTrue(os.path.isfile(sprite_path), "Expected a single global ISO 3166-2 sprite file to be created.")

        from lxml import etree
        symbol_ids = {symbol.get("id") for symbol in etree.parse(sprite_path).getroot()}
#2.)
        self.assertIn("fi-fi-fi-01", symbol_ids, "Expected symbol for FI-01 to be present in the global sprite, prefixed by its country code.")
        self.assertIn("fi-sb-sb-ml", symbol_ids, "Expected symbol for SB-ML to be present in the global sprite, prefixed by its country code.")
#3.)
        #SVG must be the default namespace (a "ns0:svg" root isn't SVG when inlined in HTML) and ids must be unique across flags
        with open(sprite_path, encoding="utf-8") as f:
            self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', f.read(), "Expected SVG as the sprite's default namespace.")
        all_ids = [el.get("id") for el in etree.parse(sprite_path).getroot().iter() if isinstance(el.tag, str) and el.get("id")]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Expected every id in the sprite to be unique.")

    # @unittest.skip("")
    def test_create_iso3166_2_svg_sprite_per_country(self):
        """ Testing generating one smaller ISO 3166-2 SVG sprite file per country. """
        sprite_dir = os.path.join(self.test_output_dir, "iso3166-2-sprites")
#1.)
        create_iso3166_2_svg_sprite(country_input_folder=os.path.join("tests", "test_flags"), per_country=True, export_sprite_dir=sprite_dir)

        #FI, IQ, KM, SB & SH sub-folders have SVG flags in the test fixture, KW only has PNGs so should be skipped
        self.assertTrue(os.path.isfile(os.path.join(sprite_dir, "fi.svg")), "Expected a per-country sprite file for FI.")
        self.assertFalse(os.path.isfile(os.path.join(sprite_dir, "kw.svg")), "Expected no sprite file for KW as it has no SVG flags.")

        from lxml import etree
        symbol_ids = {symbol.get("id") for symbol in etree.parse(os.path.join(sprite_dir, "fi.svg")).getroot()}
#2.)
        self.assertIn("fi-fi-fi-01", symbol_ids, "Expected symbol for FI-01 to be present in the FI sprite file.")

    # @unittest.skip("")
    def test_create_iso3166_3_css(self):
        """ Testing generating the ISO 3166-3 CSS file, which uses the flat-folder ISO 3166-1 generator. """
        css_path = os.path.join(self.test_output_dir, "test-iso3166-3.css")
#1.)
        create_iso3166_1_css("iso3166-3-flags", export_css_filepath=css_path, minify=True)
        with open(css_path, encoding="utf-8") as f:
            test_css_content = f.read()

        #one lower-case selector per 4-letter ISO 3166-3 code, README.MD excluded
        expected_codes = sorted(os.path.splitext(f)[0].lower() for f in os.listdir("iso3166-3-flags") if f.lower().endswith(".svg"))
        observed_codes = sorted(re.findall(r'\.fi-([a-z]{4})\s*\{', test_css_content))
        self.assertEqual(observed_codes, expected_codes, "Expected one .fi-xxxx selector per ISO 3166-3 flag.")
#2.)
        self.assertIn('.fi-cshh {\n\tbackground-image: url("../../iso3166-3-flags/CSHH.svg");', test_css_content, "Expected Czechoslovakia selector with stylesheet-relative URL.")
        self.assertTrue(os.path.isfile(os.path.join(self.test_output_dir, "test-iso3166-3.min.css")), "Expected minified ISO 3166-3 CSS file.")

    # @unittest.skip("")
    def test_css_dir_relative_urls(self):
        """ Testing flag url() paths are made relative to css_dir rather than the export location when given. """
        css_path = os.path.join(self.test_output_dir, "test-iso3166-1.css")
#1.)
        #generated into a temp location (as update_everything --check does) but served from css/
        create_iso3166_1_css(self.test_iso3166_1_flag_folder, export_css_filepath=css_path, css_dir="css")
        with open(css_path, encoding="utf-8") as f:
            test_css_content = f.read()
        self.assertIn('.fi-gb {\n\tbackground-image: url("../iso3166-1-flags/gb.svg");', test_css_content, "Expected URL relative to css_dir.")
#2.)
        create_iso3166_2_css(self.test_iso3166_2_flag_folder, export_css_filepath=css_path, css_dir="css")
        with open(css_path, encoding="utf-8") as f:
            test_css_content = f.read()
        self.assertIn('url("../iso3166-2-flags/HU/HU-HE.', test_css_content, "Expected ISO 3166-2 URL relative to css_dir.")

    # @unittest.skip("")
    def test_create_svg_sprite(self):
        """ Testing generating the ISO 3166-1 SVG sprite file. """
        sprite_path = os.path.join(self.test_output_dir, "iso3166-1-sprite.svg")
#1.)
        create_svg_sprite(country_input_folder=self.test_iso3166_1_flag_folder, export_sprite_filepath=sprite_path)

        from lxml import etree
        root = etree.parse(sprite_path).getroot()
        symbol_ids = {symbol.get("id") for symbol in root}
        expected_ids = {"fi-" + os.path.splitext(f)[0].lower() for f in os.listdir(self.test_iso3166_1_flag_folder) if f.endswith(".svg")}
        self.assertEqual(symbol_ids, expected_ids, "Expected one fi-xx symbol per ISO 3166-1 flag, including the reserved codes.")
#2.)
        #every symbol needs a viewBox to scale, and internal ids must be namespaced per flag with no dangling references
        self.assertTrue(all(symbol.get("viewBox") for symbol in root), "Expected every symbol to have a viewBox.")
        all_ids = [el.get("id") for el in root.iter() if isinstance(el.tag, str) and el.get("id")]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Expected every id in the sprite to be unique.")
        with open(sprite_path, encoding="utf-8") as f:
            sprite_content = f.read()
        refs = set(re.findall(r'url\(\s*[\'"]?#([^\'")\s]+)', sprite_content)) | set(re.findall(r'href="#([^"]+)"', sprite_content))
        self.assertFalse(refs - set(all_ids), f"Expected no references to missing ids: {sorted(refs - set(all_ids))[:5]}.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    