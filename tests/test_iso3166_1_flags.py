import unittest
import iso3166
from lxml import etree
import os
import warnings

unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("")
class ISO3166_1_Flags_Tests(unittest.TestCase):
    """
    Testing the ISO 3166-1 dataset of country flags including validating the total 
    number of flags, file extensions & formats. 
    
    test_iso3166_1_flags_total:
        testing the total number of country flags.
    test_iso3166_1_flags_file_extensions:
        testing the file extensions for the country flags.
    test_iso3166_1_flags_file_formats:
        testing the correct file name formats for the country flags.
    test_iso3166_1_flags_completeness:
        testing the list of country flags against the list of ISO 3166-1 country codes.
    test_iso3166_1_flag_duplicates:
        testing there are no duplicate country flags, mainly looking for similar flags
        but with different extension.
    test_valiate_svg_file:
        testing that each SVG file is a valid and parseable XML file.
    test_iso3166_1_flag_duplicates:
        testing there are no duplicate country flags, including those with different file extension.
    test_iso3166_1_image_dimensions:
        testing image dimensions consistency across all flags.
    test_iso3166_1_file_size_limits:
        testing file size limits to prevent accidentally huge files.
    test_iso3166_1_svg_path_complexity:
        testing SVG path complexity/optimization.
    test_iso3166_1_missing_broken_images:
        testing for missing or broken image data.
    """
    def setUp(self):      
        """ Initialise test variables. """
        self.test_input_flag_folder = "iso3166-1-flags"
        self.max_file_size_kb = 500  # 500KB max file size
        self.min_dimension = 50  # minimum width/height
        self.max_dimension = 5000  # maximum width/height

        #list of all ISO 3166-1 flags
        self.iso3166_1_files = [i for i in os.listdir(self.test_input_flag_folder) if i != "README.md" and i != ".DS_Store"]

    # @unittest.skip("")
    def test_iso3166_1_flags_total(self):
        """ Test total number of country flags. """
#1.)
        self.assertEqual(len(self.iso3166_1_files), 250, f"Expected there to be 250 flag icons in the ISO 3166-1 folder, got {len(self.iso3166_1_files)}.")

    # @unittest.skip("")
    def test_iso3166_1_flags_file_extensions(self):
        """ Test file extensions for all flags. """
#1.)
        for file in self.iso3166_1_files:
            self.assertTrue(os.path.splitext(file)[1] == ".svg", "Expected all ISO 3166-1 flag icons to be in the svg format.")

    # @unittest.skip("")
    def test_iso3166_1_flags_file_formats(self):
        """ Testing correct file naming conventions  """
#1.)
        #get list of all filenames, exclude the list of exception flags
        excluded_files = {
            "README.md", ".DS_Store",
            "gb-sct.svg", "gb-nir.svg", "gb-eng.svg", "gb-wls.svg",
            "es-ct.svg", "es-ga.svg", "es-pv.svg",
            "arab.svg", "asean.svg", "cefta.svg", "eac.svg",
            "sh-ac.svg", "sh-hl.svg", "sh-ta.svg"
        }
        iso3166_1_files = [
            fname for fname in os.listdir(self.test_input_flag_folder)
            if fname not in excluded_files
        ]

        for file in iso3166_1_files:
            self.assertTrue(len(os.path.splitext(file)[0]) == 2, f"All ISO 3166-1 flag icon filenames should be 2 letters: {file}.")
            self.assertTrue(file.islower(), f'All ISO 3166-1 flag icon filenames should be in lower-case: {file}.')

    # @unittest.skip("")
    def test_iso3166_1_flags_completeness(self):
        """ Testing the list of country flags against the list of ISO 3166-1 country codes. """
        expected_codes = list(iso3166.countries_by_alpha2.keys())
        expected_codes = [i.lower() for i in expected_codes]
        observed_codes = [os.path.splitext(f)[0] for f in self.iso3166_1_files]
        missing_codes = set(expected_codes) - set(observed_codes)
#1.)
        self.assertFalse(missing_codes, f"Expected no missing ISO 3166-1 country flags, got {missing_codes}.")
    
    # @unittest.skip("")
    def test_iso3166_1_flag_duplicates(self):
        """ Testing there are no duplicate country flags, including those with different file extension. """
        file_name_map = {}

        #iterate over flag files, parsing name and extension
        for filename in self.iso3166_1_files:
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
    def test_valiate_svg_file(self):
        """ Testing that each SVG file is a valid and parseable XML file. """
        for filename in self.iso3166_1_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    etree.parse(path)
                except Exception as e:
                    self.fail(f"{filename} is not a valid SVG file: {e}.")

    # @unittest.skip("")
    def test_iso3166_1_image_dimensions(self):
        """ Testing image dimensions consistency across all flags. """
        for filename in self.iso3166_1_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()
                    
                    #check for viewBox or width/height attributes
                    viewbox = root.get('viewBox')
                    width = root.get('width')
                    height = root.get('height')
#1.)
                    self.assertTrue(viewbox or (width and height), 
                                  f"{filename} missing viewBox or width/height attributes.")
                    
                    #if viewBox exists, validate format
                    if viewbox:
                        parts = viewbox.split()
                        self.assertEqual(len(parts), 4, f"{filename} has invalid viewBox format: {viewbox}.")
                except Exception as e:
                    self.fail(f"Error parsing dimensions for {filename}: {e}.")

    # @unittest.skip("")
    def test_iso3166_1_file_size_limits(self):
        """ Testing file size limits to prevent accidentally huge files. """
        for filename in self.iso3166_1_files:
            path = os.path.join(self.test_input_flag_folder, filename)
            file_size_kb = os.path.getsize(path) / 1024
#1.)            
            self.assertLess(file_size_kb, self.max_file_size_kb, 
                          f"{filename} exceeds max file size: {file_size_kb:.2f}KB > {self.max_file_size_kb}KB.")

    # @unittest.skip("")
    def test_iso3166_1_svg_path_complexity(self):
        """ Testing SVG path complexity/optimization. """
        max_path_elements = 1000  # reasonable limit for flag complexity
        
        for filename in self.iso3166_1_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()
                    
                    #count path elements
                    paths = root.findall(".//{http://www.w3.org/2000/svg}path")
                    path_count = len(paths)
#1.)                    
                    self.assertLess(path_count, max_path_elements, 
                                  f"{filename} has too many path elements ({path_count}), may need optimization.")
                except Exception as e:
                    self.fail(f"Error analyzing SVG complexity for {filename}: {e}.")

    # @unittest.skip("")
    def test_iso3166_1_missing_broken_images(self):
        """ Testing for missing or broken image data. """
        for filename in self.iso3166_1_files:
            path = os.path.join(self.test_input_flag_folder, filename)
#1.)            
            #check file exists and is not empty
            self.assertTrue(os.path.isfile(path), f"{filename} does not exist.")
            self.assertGreater(os.path.getsize(path), 0, f"{filename} is empty (0 bytes).")
            
            #for SVG, check it has actual content
            if filename.endswith(".svg"):
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()
                    
                    #check SVG has child elements
                    children = list(root)
                    self.assertGreater(len(children), 0, f"{filename} has no child elements.")
                except Exception as e:
                    self.fail(f"{filename} is corrupted or invalid: {e}.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()