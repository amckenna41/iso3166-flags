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
    test_iso3166_2_flag_organization:
        testing flag organization by country folder.
    test_iso3166_2_no_orphaned_flags:
        testing there are no orphaned flags (files without matching subdivision codes).
    test_iso3166_2_aspect_ratios_per_country:
        testing consistent aspect ratios per country.
    test_iso3166_2_flag_naming_matches_folder:
        testing flag naming matches parent folder.
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
        
        #create mapping of files to their parent folders
        self.file_folder_map = {}
        for root, _, files in os.walk(self.test_input_flag_folder):
            for f in files:
                if f not in ("README.md", ".DS_Store"):
                    parent_folder = os.path.basename(root)
                    self.file_folder_map[f] = parent_folder

    # @unittest.skip("")
    def test_iso3166_2_flags_total(self):
        """ Test total number of subdivision flags. """
#1.)
        self.assertEqual(len(self.iso3166_2_files), 2843, f"Expected there to be 2843 flags in the ISO 3166-2 folder, got {len(self.iso3166_2_files)}.")

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

    # @unittest.skip("")
    def test_iso3166_2_flag_organization(self):
        """ Testing flag organization by country folder. """
        #get all country folders
        country_folders = [f for f in os.listdir(self.test_input_flag_folder) 
                          if os.path.isdir(os.path.join(self.test_input_flag_folder, f)) and f != ".DS_Store"]
#1.)        
        #verify each country folder contains at least one flag
        for folder in country_folders:
            folder_path = os.path.join(self.test_input_flag_folder, folder)
            files = [f for f in os.listdir(folder_path) if f not in ("README.md", ".DS_Store")]
            self.assertGreater(len(files), 0, f"Country folder {folder} is empty.")
            
            #verify folder names are uppercase 2-letter codes
            self.assertEqual(len(folder), 2, f"Country folder {folder} should be 2 letters.")
            self.assertTrue(folder.isupper(), f"Country folder {folder} should be uppercase.")

    # @unittest.skip("")
    def test_iso3166_2_no_orphaned_flags(self):
        """ Testing there are no orphaned flags (files without matching subdivision codes). """
        subdivisions = Subdivisions()
        all_subdivision_codes = subdivisions.subdivision_codes()
        
        orphaned_flags = []
        
        for filename in self.iso3166_2_files:
            subdivision_code = os.path.splitext(filename)[0]
            country_code = subdivision_code.split('-')[0]
            
            #check if subdivision code exists in iso3166-2 data
            if country_code in all_subdivision_codes:
                if subdivision_code not in all_subdivision_codes[country_code]:
                    orphaned_flags.append(filename)
            else:
                orphaned_flags.append(filename)
#1.)        
        self.assertEqual(len(orphaned_flags), 0, 
                        f"Found {len(orphaned_flags)} orphaned flags without matching subdivision codes: {orphaned_flags[:10]}")

    # @unittest.skip("")
    def test_iso3166_2_aspect_ratios_per_country(self):
        """ Testing consistent aspect ratios per country. """
        country_aspect_ratios = {}
        
        for root, _, files in os.walk(self.test_input_flag_folder):
            parent_folder = os.path.basename(root)
            
            #skip the main directory
            if parent_folder == os.path.basename(self.test_input_flag_folder):
                continue
                
            for filename in files:
                if filename.endswith(".svg") and filename not in ("README.md", ".DS_Store"):
                    path = os.path.join(root, filename)
                    try:
                        tree = etree.parse(path)
                        root_elem = tree.getroot()
                        
                        #get viewBox or width/height
                        viewbox = root_elem.get('viewBox')
                        if viewbox:
                            parts = viewbox.split()
                            if len(parts) == 4:
                                width = float(parts[2])
                                height = float(parts[3])
                                aspect_ratio = round(width / height, 2)
                                
                                if parent_folder not in country_aspect_ratios:
                                    country_aspect_ratios[parent_folder] = []
                                country_aspect_ratios[parent_folder].append((filename, aspect_ratio))
                    except:
                        pass
        
        #check for excessive variation in aspect ratios within a country
        inconsistent_countries = []
        for country, ratios in country_aspect_ratios.items():
            if len(ratios) > 1:
                aspect_values = [r[1] for r in ratios]
                #allow some variation but flag if range is too large
                if max(aspect_values) - min(aspect_values) > 1.5:
                    inconsistent_countries.append((country, ratios))
#1.)        
        #this is a warning-level test, not a hard failure
        if inconsistent_countries:
            print(f"\nWarning: {len(inconsistent_countries)} countries have varying aspect ratios: {[c[0] for c in inconsistent_countries[:5]]}")

    # @unittest.skip("")
    def test_iso3166_2_flag_naming_matches_folder(self):
        """ Testing flag naming matches parent folder. """
        mismatched_flags = []
        
        for filename, parent_folder in self.file_folder_map.items():
            subdivision_code = os.path.splitext(filename)[0]
            country_code_from_file = subdivision_code.split('-')[0]
            
            #verify country code in filename matches parent folder
            if country_code_from_file != parent_folder:
                mismatched_flags.append(f"{filename} in {parent_folder}/")
#1.)        
        self.assertEqual(len(mismatched_flags), 0, 
                        f"Found {len(mismatched_flags)} flags in wrong folders: {mismatched_flags[:10]}")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()