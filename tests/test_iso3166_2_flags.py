import unittest
import os
import re
from lxml import etree
from iso3166_2 import Subdivisions
import warnings

unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("")
class ISO3166_2_Flags_Tests(unittest.TestCase):
    """
    Testing the ISO 3166-2 dataset of regional/subdivision flags including validating 
    the total number of flags, file extensions & formats. 
    
    test_iso3166_2_flags_total:
        testing the total number of subdivision flags.
    test_iso3166_2_flags_file_extensions:
        testing the file extensions for the subdivision flags.
    test_iso3166_2_flags_file_formats:
        testing the correct file name formats for the subdivision flags.
    test_iso3166_2_subdivision_codes:
        testing each subdivision flag filename is a valid subdivision code in iso3166-2 software.
    test_valiate_svg_file:
        testing that each SVG file is a valid and parseable XML file.
    test_iso3166_2_flag_duplicates:
        testing there are no duplicate country flags, including those with different file extension.
    """
    def setUp(self):      
        """ Initialise test variables. """
        self.test_input_flag_folder = "iso3166-2-flags"

        #list of all ISO 3166-2 subdivision flags
        self.iso3166_2_files = [
            f
            for _, _, files in os.walk(self.test_input_flag_folder)
            for f in files
            if f not in ("README.md", ".DS_Store")
        ]

    # @unittest.skip("")
    def test_iso3166_2_flags_total(self):
        """ Test total number of subdivision flags. """
#1.)
        self.assertEqual(len(self.iso3166_2_files), 2845, f"Expected there to be 2845 flags in the ISO 3166-2 folder, got {len(self.iso3166_2_files)}.")

    # @unittest.skip("")
    def test_iso3166_2_flags_file_extensions(self):
        """ Test file extensions for all flags. """
#1.)    
        valid_formats = [".svg", ".png", ".jpg", ".jpeg"]
        for file in self.iso3166_2_files:
            self.assertTrue(os.path.splitext(file)[1] in valid_formats, f"Expected all ISO 3166-2 flag icons to be in one of the valid formats: {valid_formats}.")

    # @unittest.skip("")
    def test_iso3166_2_flags_file_formats(self):
        """ Testing correct file naming conventions  """
#1.)
        for file in self.iso3166_2_files:
            subdivision_filename = os.path.splitext(file)[0]
            self.assertTrue(bool(re.match(r"^[A-Z][A-Z]-[A-Z0-9]$|^[A-Z][A-Z]-[A-Z0-9][A-Z0-9]$|[A-Z][A-Z]-[A-Z0-9][A-Z0-9][A-Z0-9]$", subdivision_filename)), 
                    f"Subdivision filename does not match expected format: XX-YYY, XX-YY or XX-Y, where XX is the alpha-2 country code and Y is the ISO 3166-2 subdivision code {file}.")
            self.assertTrue(subdivision_filename.isupper(), 'All ISO 3166-2 flag icon filenames should be in upper-case.')
    
    # @unittest.skip("")
    def test_iso3166_2_subdivision_codes(self):
        """ Testing each subdivision flag filename is a valid subdivision code in iso3166-2 software. """
        observed_subdivision_codes = [os.path.splitext(f)[0] for f in self.iso3166_2_files]
        subdivisions = Subdivisions()
        all_subdivision_codes = subdivisions.subdivision_codes()
#1.)
        for code in observed_subdivision_codes:
            country_code = code.split('-')[0]
            self.assertTrue(code in all_subdivision_codes[country_code], 
                f"Expected subdivision code of flag file to be in list of subdivision codes: {all_subdivision_codes[country_code]}.")

    # @unittest.skip("")
    def test_valiate_svg_file(self):
        """ Testing that each SVG file is a valid and parseable XML file. """
        for filename in self.iso3166_2_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, os.path.splitext(filename)[0].split('-')[0], filename)
                try:
                    etree.parse(path)
                except Exception as e:
                    self.fail(f"{filename} is not a valid SVG file: {e}.")

    # @unittest.skip("")
    def test_iso3166_2_flag_duplicates(self):
        """ Testing there are no duplicate subdivision flags, including those with different file extension. """
        file_name_map = {}

        #iterate over flag files, parsing name and extension
        for filename in self.iso3166_2_files:
            name, ext = os.path.splitext(filename)

            #add filename and extension to object
            if name not in file_name_map:
                file_name_map[name] = [ext]
            else:
                file_name_map[name].append(ext)

        #create object of duplicate files, if applicable
        duplicates = {name: exts for name, exts in file_name_map.items() if len(exts) > 1}
#1.)
        self.assertFalse(duplicates, f"Expected no flags with no duplicate base names across extensions, got: {duplicates}.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()