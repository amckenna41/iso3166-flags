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
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_iso3166_1_flag_folder = "iso3166-1-flags"
        self.test_iso3166_2_flag_folder = "iso3166-2-flags"
        self.subdivisions = Subdivisions()

        #create test directory if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

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
        country_code_exceptions = ["gb-nir", "gb-sct", "gb-wls", "gb-eng", "ac", "ta", "cp", "dg", "ic", "xk", "xx", "un", "eu", "pc"]

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

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    