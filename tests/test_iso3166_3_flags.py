import unittest
import re
import os
import warnings
from lxml import etree

unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

#complete set of ISO 3166-3 alpha-4 codes defined by the standard.
#first two characters are the former ISO 3166-1 alpha-2 code of the deleted country;
#last two characters are either the successor country's alpha-2 code or "HH" where no
#single successor exists (dissolved, merged into multiple states, or territory absorbed).
KNOWN_ISO3166_3_CODES = {
    "AIDJ",  # French Territory of the Afars and Issas  → Djibouti (DJ)
    "ANHH",  # Netherlands Antilles                     → dissolved (CW, SX, BQ)
    "BQAQ",  # British Antarctic Territory              → Antarctica (AQ)
    "BUMM",  # Burma                                   → Myanmar (MM)
    "BYAA",  # Byelorussian SSR                        → Belarus (BY)
    "CSHH",  # Czechoslovakia                          → Czech Republic (CZ), Slovakia (SK)
    "CSXX",  # Serbia and Montenegro                   → Serbia (RS), Montenegro (ME)
    "CTKI",  # Canton and Enderbury Islands            → Kiribati (KI)
    "DDDE",  # German Democratic Republic (East Germany) → Germany (DE)
    "DYBJ",  # Dahomey                                 → Benin (BJ)
    "FQHH",  # French Southern and Antarctic Territories → TF / HM
    "FXFR",  # Metropolitan France                     → France (FR)
    "GEHH",  # Gilbert and Ellice Islands              → Kiribati (KI), Tuvalu (TV)
    "HVBF",  # Upper Volta                             → Burkina Faso (BF)
    "JTUM",  # Johnston Island                         → US Minor Outlying Islands (UM)
    "MIHH",  # Midway Islands                          → US Minor Outlying Islands (UM)
    "NHVU",  # New Hebrides                            → Vanuatu (VU)
    "NQAQ",  # Dronning Maud Land                     → Antarctica (AQ)
    "PCHH",  # Pacific Islands Trust Territory         → FM, MH, MP, PW
    "PUUM",  # US Miscellaneous Pacific Islands        → US Minor Outlying Islands (UM)
    "PZPA",  # Panama Canal Zone                       → Panama (PA)
    "RHZW",  # Rhodesia                                → Zimbabwe (ZW)
    "SKIN",  # Sikkim                                  → India (IN)
    "SUHH",  # Soviet Union (USSR)                     → Russia (RU) + 14 republics
    "TPTL",  # Portuguese Timor / East Timor           → Timor-Leste (TL)
    "VDVN",  # Democratic Republic of Vietnam          → Vietnam (VN)
    "WKUM",  # Wake Island                             → US Minor Outlying Islands (UM)
    "YDYE",  # South Yemen                             → Yemen (YE)
    "YUCS",  # Yugoslavia                              → BA, HR, MK, ME, RS, SI
    "ZRCD",  # Zaire                                   → DR Congo (CD)
}

# @unittest.skip("")
class ISO3166_3_Flags_Tests(unittest.TestCase):
    """
    Testing the ISO 3166-3 dataset of former country flags including validating the
    total number of flags, file extensions, naming conventions, and SVG integrity.

    test_iso3166_3_flags_total:
        testing the total number of former country flags.
    test_iso3166_3_flags_file_extensions:
        testing that all flags are in SVG format.
    test_iso3166_3_flags_file_formats:
        testing the correct alpha-4 filename format for each flag.
    test_iso3166_3_flags_valid_codes:
        testing each alpha-4 code in the folder is a known ISO 3166-3 code.
    test_iso3166_3_flag_duplicates:
        testing there are no duplicate flags with the same base name.
    test_validate_svg_file:
        testing that each SVG file is a valid and parseable XML file.
    test_iso3166_3_image_dimensions:
        testing SVG files have viewBox or width/height attributes.
    test_iso3166_3_file_size_limits:
        testing file size limits to prevent accidentally huge files.
    test_iso3166_3_svg_path_complexity:
        testing SVG path complexity/optimization.
    test_iso3166_3_missing_broken_images:
        testing for missing or broken image data.
    """
    def setUp(self):
        """ Initialise test variables. """
        self.test_input_flag_folder = "iso3166-3-flags"
        self.max_file_size_kb = 1000  # 1000KB max file size (historical SVGs can be more detailed than modern flags)
        self.max_path_elements = 1000  # reasonable limit for flag SVG complexity

        #list of all ISO 3166-3 flag files, excluding non-flag files
        self.iso3166_3_files = [
            f for f in os.listdir(self.test_input_flag_folder)
            if f not in ("README.MD", "README.md", ".DS_Store")
        ]

    # @unittest.skip("")
    def test_iso3166_3_flags_total(self):
        """ Test total number of former country flags. """
#1.)
        self.assertEqual(len(self.iso3166_3_files), 24,
            f"Expected 24 flag icons in the ISO 3166-3 folder, got {len(self.iso3166_3_files)}.")

    # @unittest.skip("")
    def test_iso3166_3_flags_file_extensions(self):
        """ Test that all flags are in SVG format. """
#1.)
        for file in self.iso3166_3_files:
            self.assertEqual(os.path.splitext(file)[1], ".svg",
                f"Expected all ISO 3166-3 flag icons to be in SVG format, got: {file}.")

    # @unittest.skip("")
    def test_iso3166_3_flags_file_formats(self):
        """ Testing correct alpha-4 filename naming convention. """
#1.)
        for file in self.iso3166_3_files:
            name = os.path.splitext(file)[0]
            self.assertTrue(bool(re.match(r'^[A-Z]{4}$', name)),
                f"ISO 3166-3 flag filename must be exactly 4 uppercase letters (alpha-4 code), got: {file}.")
            self.assertTrue(name.isupper(),
                f"ISO 3166-3 flag icon filenames must be uppercase: {file}.")

    # @unittest.skip("")
    def test_iso3166_3_flags_valid_codes(self):
        """ Testing each alpha-4 code in the folder is a known ISO 3166-3 code. """
#1.)
        for file in self.iso3166_3_files:
            code = os.path.splitext(file)[0]
            self.assertIn(code, KNOWN_ISO3166_3_CODES,
                f"'{code}' is not a recognised ISO 3166-3 alpha-4 code. "
                f"Update KNOWN_ISO3166_3_CODES if this is a newly added entry.")

    # @unittest.skip("")
    def test_iso3166_3_flag_duplicates(self):
        """ Testing there are no duplicate flags with the same base name. """
        file_name_map = {}

        #iterate over flag files, parsing name and extension
        for filename in self.iso3166_3_files:
            name, ext = os.path.splitext(filename)
            if name not in file_name_map:
                file_name_map[name] = [ext]
            else:
                file_name_map[name].append(ext)

        #build object of duplicate entries
        duplicates = {name: exts for name, exts in file_name_map.items() if len(exts) > 1}
#1.)
        self.assertFalse(duplicates,
            f"Expected no duplicate base names across extensions, got: {duplicates}.")

    # @unittest.skip("")
    def test_validate_svg_file(self):
        """ Testing that each SVG file is a valid and parseable XML file. """
        for filename in self.iso3166_3_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    etree.parse(path)
                except Exception as e:
                    self.fail(f"{filename} is not a valid SVG/XML file: {e}.")

    # @unittest.skip("")
    def test_iso3166_3_image_dimensions(self):
        """ Testing SVG files have viewBox or width/height attributes. """
        for filename in self.iso3166_3_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()

                    viewbox = root.get('viewBox')
                    width   = root.get('width')
                    height  = root.get('height')
#1.)
                    self.assertTrue(viewbox or (width and height),
                        f"{filename} is missing both viewBox and width/height attributes.")

                    #if viewBox present, validate it has exactly 4 numeric parts
                    if viewbox:
                        parts = viewbox.split()
                        self.assertEqual(len(parts), 4,
                            f"{filename} has an invalid viewBox format: '{viewbox}'.")
                except Exception as e:
                    self.fail(f"Error parsing dimensions for {filename}: {e}.")

    # @unittest.skip("")
    def test_iso3166_3_file_size_limits(self):
        """ Testing file size limits to prevent accidentally huge files. """
        for filename in self.iso3166_3_files:
            path = os.path.join(self.test_input_flag_folder, filename)
            file_size_kb = os.path.getsize(path) / 1024
#1.)
            self.assertLess(file_size_kb, self.max_file_size_kb,
                f"{filename} exceeds the maximum allowed file size: "
                f"{file_size_kb:.2f}KB > {self.max_file_size_kb}KB.")

    # @unittest.skip("")
    def test_iso3166_3_svg_path_complexity(self):
        """ Testing SVG path complexity to catch unoptimised files. """
        for filename in self.iso3166_3_files:
            if filename.endswith(".svg"):
                path = os.path.join(self.test_input_flag_folder, filename)
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()
                    path_elements = root.findall(".//{http://www.w3.org/2000/svg}path")
#1.)
                    self.assertLess(len(path_elements), self.max_path_elements,
                        f"{filename} has {len(path_elements)} path elements, "
                        f"which exceeds the limit of {self.max_path_elements} — consider optimising with svgo.")
                except Exception as e:
                    self.fail(f"Error analysing SVG complexity for {filename}: {e}.")

    # @unittest.skip("")
    def test_iso3166_3_missing_broken_images(self):
        """ Testing for missing or broken image data. """
        for filename in self.iso3166_3_files:
            path = os.path.join(self.test_input_flag_folder, filename)
#1.)
            self.assertTrue(os.path.isfile(path),
                f"{filename} does not exist at expected path: {path}.")
            self.assertGreater(os.path.getsize(path), 0,
                f"{filename} is empty (0 bytes).")

            #for SVG files, verify the document has at least one child element
            if filename.endswith(".svg"):
                try:
                    tree = etree.parse(path)
                    root = tree.getroot()
                    self.assertGreater(len(list(root)), 0,
                        f"{filename} parses as valid XML but contains no child elements.")
                except Exception as e:
                    self.fail(f"{filename} is corrupted or invalid: {e}.")

if __name__ == '__main__':
    #run all unit tests
    unittest.main()
