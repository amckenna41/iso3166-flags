from scripts.get_missing_flags import *
import shutil
import os
import random
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Missing_Flags_Tests(unittest.TestCase):
    """
    Test suite for testing get_missing_flags.py script that exports a list of all 
    subdivisions that do not have an associated flag in the repo.

    Test Cases
    ==========
    test_get_missing_flags:
        testing the main function for exporting the list of subdivisions with no flag
        in repo.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_missing_flags_output = os.path.join(self.test_output_dir, "test_missing_flags.csv")
        self.test_flag_icons_dir = "iso3166-2-flags"

        #create test directory if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

    # @unittest.skip("")
    def test_get_missing_flags(self):
        """ Testing the main function for exporting the list of subdivisions with no flag in repo. """
#1.)
        test_missing_flags = export_missing_flags(self.test_flag_icons_dir, export=True, export_filename=self.test_missing_flags_output)

        #list of all file names
        test_all_files = []

        #iterate through the flag folder & sub-folders (if applicable) - getting list of file names
        for _, _, filenames in os.walk(self.test_flag_icons_dir):
                
            #iterate over the filenames in the current folder
            for filename in filenames:
                #skip markdown files
                if (filename == "README.md"):
                    continue
                #add the filename, without its extension, to the dictionary under the parent folder key
                test_all_files.append(os.path.splitext(filename)[0])

        #random valid and invalid subdivision codes
        random_valid_subdivision_codes = ['AF-TAK', 'AM-AR', 'GB-WOK', 'ID-ML', 'IR-02', 'LY-WD', 'MA-03', 'ML-1', 'RS-24', 'RW-03']
        random_invalid_subdivision_codes = random.sample(test_all_files, 10)

        self.assertEqual(len(test_missing_flags), 2204, f"Expected there to be 2204 rows in missing flags dataframe, got {len(test_missing_flags)}.")
        self.assertEqual(list(test_missing_flags.columns), ["subdivisionCode", "subdivisionName", "subdivisionType"], f"Expected and observed column names of dataframe don't match {list(test_missing_flags.columns)}.")
        self.assertTrue(os.path.isfile(self.test_missing_flags_output), "Expected missing subdivision flags output to exist in folder.")

        #validate that random list of valid and invalid codes should & shouldn't be in output dataframe
        for code in random_valid_subdivision_codes:
            self.assertIn(code, test_missing_flags['subdivisionCode'].values, f"Expected subdivision code {code} to be in subdivisionCode column.")
        for code in random_invalid_subdivision_codes:
            self.assertNotIn(code, test_missing_flags['subdivisionCode'].values, f"Expected subdivision code {code} not to be in subdivisionCode column.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    