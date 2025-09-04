from scripts.get_flag_metadata import *
import shutil
import os
import json
from iso3166_2 import *
from pandas.testing import assert_frame_equal
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Flag_Metadata_Tests(unittest.TestCase):
    """
    Test suite for testing get_flag_metadata.py script that exports a plethora of 
    metadata for all of the country and subdivision flags. 

    Test Cases
    ==========
    test_export_flag_metadata:
        testing full pipeline for exporting the flag metadata.
    test_calculate_dimension:
        testing calculating the width/height of an image.
    test_calculate_quality:
        testing calculating the image quality of an image.
    test_get_file_info:
        testing getting the file info of an image.
    calculate_svg_dimension:
        testing getting the file metadata for SVG images.
    test_parse_svg_dimension:
        testing getting the dimensions for SVG images.
    test_export_repo_metadata:
        testing getting a plethora of data attributes for the repo.
    test_export_flag_list:
        testing the exporting of the full list of ISO 3166-2 subdivisions
        and whether they have flags 
    test_filter_by_size:
        testing the filtering of the image files per an input KB size threshold.
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_flag_folder = os.path.join("tests", "test_flags")
        self.test_threshold_file = os.path.join(self.test_output_dir, "test_file_threshold.csv")
        self.test_flag_metadata_output = os.path.join(self.test_output_dir, "test_flag_metadata.csv")
        self.test_repo_metadata_output = os.path.join(self.test_output_dir, "test_repo_metadata.json")

        #create test directory if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

#     @unittest.skip("")
    def test_export_flag_metadata(self):
        """ Testing full pipeline for exporting the flag metadata. """
        export_flag_metadata(self.test_flag_folder, self.test_flag_metadata_output)

        export_flag_metadata("iso3166-2-flags", self.test_flag_metadata_output)

        test_flag_metadata_df = pd.read_csv(self.test_flag_metadata_output)
        subdivision_codes_subset = ["FI-07", "IQ-AR", "KM-A", "SB-ML", "SH-HL", "WF-UV"]
        test_flag_metadata_observed = test_flag_metadata_df[test_flag_metadata_df["subdivision_code"].isin(subdivision_codes_subset)]
#1.)
        self.assertTrue(os.path.isfile(self.test_flag_metadata_output), "Expected output metadata file to be exported.")  
#2.)  
        test_flag_metadata_expected = pd.DataFrame([
            ["FI-07", "FI-07.svg", 30.95, "SVG", "(700, 1000)", 1.43, None, 100.0],
            ["IQ-AR", "IQ-AR.png", 156.844, "PNG", "(1200, 1800)", 1.50, None, 3.9],
            ["KM-A",  "KM-A.svg", 0.502, "SVG", "(400, 600)", 1.5, None, 8.0],
            ["SB-ML", "SB-ML.svg", 35.128, "SVG", "(256, 512)", 2.0, None, 100.0],
            ["SH-HL", "SH-HL.svg", 84.881, "SVG", "(600, 1200)", 2.0, None, 100.0],
            ["WF-UV", "WF-UV.svg", 0.851, "SVG", "(600, 900)", 1.5, None, 12.0],
        ], columns=test_flag_metadata_observed.columns)
        
        try:
           pd.testing.assert_frame_equal(test_flag_metadata_observed.reset_index(drop=True), test_flag_metadata_expected.reset_index(drop=True), check_dtype=False)
        except AssertionError as e:
           raise AssertionError(f"Observed and expected flag metadata output DataFrame do not match:\n{str(e)}")
#3.)
        with self.assertRaises(OSError):
            export_flag_metadata("invalid_folder")
            export_flag_metadata("invalid_folder1")

#     @unittest.skip("")
    def test_calculate_dimension(self):
        """ Testing calculating the width/height of an image. """
        test_flag_filepath1 = self.test_flag_folder + "/IQ/IQ-AN.png"
        test_flag_filepath2 = self.test_flag_folder + "/IQ/IQ-KI.png"
        test_flag_filepath3 = self.test_flag_folder + "/KW/KW-AH.png"
        test_flag_filepath4 = self.test_flag_folder + "/KW/KW-MU.png"
#1.)    
        test_image_dimensions = calculate_dimension(test_flag_filepath1)
        self.assertEqual((1280, 809, 1.58), test_image_dimensions, f"Expected and observed image dimensions do not match: {test_image_dimensions}.")
#2.)
        test_image_dimensions = calculate_dimension(test_flag_filepath2)
        self.assertEqual((1280, 854, 1.5), test_image_dimensions, f"Expected and observed image dimensions do not match: {test_image_dimensions}.")
#3.)
        test_image_dimensions = calculate_dimension(test_flag_filepath3)
        self.assertEqual((288, 216, 1.33), test_image_dimensions, f"Expected and observed image dimensions do not match: {test_image_dimensions}.")
#4.)
        test_image_dimensions = calculate_dimension(test_flag_filepath4)
        self.assertEqual((288, 216, 1.33), test_image_dimensions, f"Expected and observed image dimensions do not match: {test_image_dimensions}.")
#5.)
        with self.assertRaises(FileNotFoundError):
            calculate_dimension("invalid_filepath")
            calculate_dimension("invalid_filepath2")
#6.)
        with self.assertRaises(ValueError):
            calculate_dimension(self.test_flag_folder + "/FI/FI-02.svg")
            calculate_dimension(self.test_flag_folder + "/IQ/IQ-SD.svg")
            calculate_dimension(self.test_flag_folder + "/KM/KM-M.svg")

#     @unittest.skip("")
    def test_calculate_quality(self):
        """ Testing calculating the image quality of an image. """
        test_flag_filepath1 = self.test_flag_folder + "/IQ/IQ-NA.png"
        test_flag_filepath2 = self.test_flag_folder + "/KW/KW-MU.png"
        test_flag_filepath3 = self.test_flag_folder + "/SB/SB-IS.png"
        test_flag_filepath4 = self.test_flag_folder + "/SB/SB-WE.png"
#1.)
        test_flag_filepath1_quality = calculate_quality(test_flag_filepath1)
        self.assertEqual(test_flag_filepath1_quality, 2.56, f"Expected and observed image quality values do not match: {test_flag_filepath1_quality}.")
#2.)
        test_flag_filepath2_quality = calculate_quality(test_flag_filepath2)
        self.assertEqual(test_flag_filepath2_quality, 48.7, f"Expected and observed image quality values do not match: {test_flag_filepath2_quality}.")
#3.)
        test_flag_filepath3_quality = calculate_quality(test_flag_filepath3)
        self.assertEqual(test_flag_filepath3_quality, 3.68, f"Expected and observed image quality values do not match: {test_flag_filepath3_quality}.")
#4.)
        test_flag_filepath4_quality = calculate_quality(test_flag_filepath4)
        self.assertEqual(test_flag_filepath4_quality, 9.18, f"Expected and observed image quality values do not match: {test_flag_filepath4_quality}.")
#5.)
        with self.assertRaises(FileNotFoundError):
            calculate_quality("invalid_filepath")
            calculate_quality("invalid_filepath2")
#6.)
        with self.assertRaises(ValueError):
            calculate_dimension(self.test_flag_folder + "/FI/FI-02.svg")
            calculate_dimension(self.test_flag_folder + "/IQ/IQ-SD.svg")
            calculate_dimension(self.test_flag_folder + "/KM/KM-M.svg")

#     @unittest.skip("")
    def test_get_file_info(self):
        """ Testing getting the file info of an image. """
        test_flag_filepath1 = self.test_flag_folder + "/FI/FI-09.svg"
        test_flag_filepath2 = self.test_flag_folder + "/KM/KM-M.svg"
        test_flag_filepath3 = self.test_flag_folder + "/SB/SB-TE.svg"
        test_flag_filepath4 = self.test_flag_folder + "/WF/WF-UV.svg"
#1.)
        test_flag_info = get_file_info(test_flag_filepath1)
        test_flag_info_expected = {'subdivision_code': 'Fi-09', 'file_name': 'Fi-09.svg', 'file_size_kb': 15.111, 'file_extension': 'SVG', 
                                   'dimensions': (624, 566), 'aspect_ratio': 0.91, 'flag_type': None, 'quality': 24}
        self.assertEqual(test_flag_info, test_flag_info_expected, f"Expected and observed flag info object do not match:\n{test_flag_info}.")
#2.)
        test_flag_info = get_file_info(test_flag_filepath2)
        test_flag_info_expected = {'subdivision_code': 'KM-M', 'file_name': 'KM-M.svg', 'file_size_kb': 0.457, 'file_extension': 'SVG', 
                                   'dimensions': (400, 600), 'aspect_ratio': 1.5, 'flag_type': None, 'quality': 4}
        self.assertEqual(test_flag_info, test_flag_info_expected, f"Expected and observed flag info object do not match:\n{test_flag_info}.")
#3.)
        test_flag_info = get_file_info(test_flag_filepath3)
        test_flag_info_expected = {'subdivision_code': 'SB-TE', 'file_name': 'SB-TE.svg', 'file_size_kb': 6.034, 'file_extension': 'SVG', 
                                   'dimensions': (600, 1200), 'aspect_ratio': 2.0, 'flag_type': None, 'quality': 18}
        self.assertEqual(test_flag_info, test_flag_info_expected, f"Expected and observed flag info object do not match:\n{test_flag_info}.")
#4.)
        test_flag_info = get_file_info(test_flag_filepath4)
        test_flag_info_expected = {'subdivision_code': 'WF-UV', 'file_name': 'WF-UV.svg', 'file_size_kb': 0.851, 'file_extension': 'SVG', 
                                   'dimensions': (600, 900), 'aspect_ratio': 1.5, 'flag_type': None, 'quality': 12}
        self.assertEqual(test_flag_info, test_flag_info_expected, f"Expected and observed flag info object do not match:\n{test_flag_info}.")
#5.)
        with self.assertRaises(OSError):
            get_file_info("invalid_filepath.svg")
            get_file_info("invalid_filepath2.svg")

#     @unittest.skip("")
    def test_get_svg_metadata(self):
        """ Testing getting the file metadata for SVG images. """
        test_svg_filepath1 = self.test_flag_folder + "/FI/FI-19.svg"
        test_svg_filepath2 = self.test_flag_folder + "/KM/KM-G.svg"
        test_svg_filepath3 = self.test_flag_folder + "/SB/SB-RB.svg"
        test_svg_filepath4 = self.test_flag_folder + "/SH/SH-TA.svg"
#1.)    
        test_svg_filepath1_metadata = calculate_svg_dimension(test_svg_filepath1)
        self.assertEqual(test_svg_filepath1_metadata, (500, 690, 0.72), f"Expected and observed SVG image dimension do not match: {test_svg_filepath1_metadata}.")
#2.)
        test_svg_filepath2_metadata = calculate_svg_dimension(test_svg_filepath2)
        self.assertEqual(test_svg_filepath2_metadata, (731, 487, 1.5), f"Expected and observed SVG image dimension do not match: {test_svg_filepath2_metadata}.")
#3.)
        test_svg_filepath3_metadata = calculate_svg_dimension(test_svg_filepath3)
        self.assertEqual(test_svg_filepath3_metadata, (1200, 600, 2.0), f"Expected and observed SVG image dimension do not match: {test_svg_filepath3_metadata}.")
#4.)
        test_svg_filepath4_metadata = calculate_svg_dimension(test_svg_filepath4)
        self.assertEqual(test_svg_filepath4_metadata, (1000, 500, 2.0), f"Expected and observed SVG image dimension do not match: {test_svg_filepath4_metadata}.")
#5.)
        with self.assertRaises(OSError):
            calculate_svg_dimension("invalid_filepath.svg")
            calculate_svg_dimension("invalid_filepath2.svg")

#     @unittest.skip("")
    def test_parse_svg_dimensions(self):
        """ Testing getting the dimensions for SVG images. """
        test_svg_dimesion_1 = "100px"
        test_svg_dimesion_2 = "5cm"
        test_svg_dimesion_3 = "1.5in"
        test_svg_dimesion_4 = "30%"
#1.)
        test_svg_dimesion_output1 = parse_svg_dimension(test_svg_dimesion_1)
        self.assertEqual(test_svg_dimesion_output1, 100.0, f"Expected and observed SVG dimension ouput do not match: {test_svg_dimesion_output1}.")
#2.)
        test_svg_dimesion_output2 = parse_svg_dimension(test_svg_dimesion_2)
        self.assertEqual(test_svg_dimesion_output2, 188.976, f"Expected and observed SVG dimension ouput do not match: {test_svg_dimesion_output2}.")
#3.)
        test_svg_dimesion_output3 = parse_svg_dimension(test_svg_dimesion_3)
        self.assertEqual(test_svg_dimesion_output3, 144.0, f"Expected and observed SVG dimension ouput do not match: {test_svg_dimesion_output3}.")
#4.)
        with self.assertRaises(ValueError):
                test_svg_dimesion_output4 = parse_svg_dimension(test_svg_dimesion_4)

#     @unittest.skip("")
    def test_export_repo_metadata(self):
        """ Testing getting a plethora of data attributes for the repo. """
#1.)    
        test_repo_metadata = export_repo_metadata(export_json=True, export_filename=self.test_repo_metadata_output)
        test_repo_metadata_expected = {'total': 3116, 'iso3166_1_total': 271, 'iso3166_2_total': 2845, 'svg': 2264, 'png': 798, 'jpg/jpeg': 54, 'other': 0, 'duplicates': 0, 
                                       'subdivisions_other': [], 'duplicate_list': [], 'total_repo_size': '341,605.940KB', 'iso3166_1_flags_size': '1,955.571KB', 
                                       'iso3166_2_flags_size': '339,650.369KB', 'average_flag_size': '112,260.746KB', 'missing_iso3166_1_count': 0, 'missing_iso3166_2_count': 2204}

        self.assertTrue(os.path.isfile(self.test_repo_metadata_output), "Expected flag metadata format output file to be exported.")
        #open exported metadata json
        with open(self.test_repo_metadata_output) as output_json:
            test_repo_metadata_output_json = json.load(output_json)

        self.assertEqual(test_repo_metadata_output_json, test_repo_metadata_expected, f"Expected and observed metadata object do not match:\n{test_repo_metadata_output_json}")
        self.assertEqual(test_repo_metadata_output_json["total"], (test_repo_metadata_output_json["iso3166_1_total"] + test_repo_metadata_output_json["iso3166_2_total"]), 
                "Expected 'iso3166_1_total' and 'iso3166_2_total' attributes to summate to the value of the 'total' attribute.")
        self.assertEqual(test_repo_metadata_output_json["total"], (test_repo_metadata_output_json["svg"] + test_repo_metadata_output_json["png"] + test_repo_metadata_output_json["jpg/jpeg"]
                + test_repo_metadata_output_json["other"]), "Expected individual count of the image formats to summate to the total number of files in the repo.")
        self.assertAlmostEqual(float(test_repo_metadata_output_json["total_repo_size"].replace('KB', '').replace(',', '')), (float(test_repo_metadata_output_json["iso3166_1_flags_size"].replace('KB', '').replace(',', '')) + 
                float(test_repo_metadata_output_json["iso3166_2_flags_size"].replace('KB', '').replace(',', ''))), places=2, msg="Expected the individual directory sizes in KB to add up to the 'total' folder size attribute.")
        self.assertEqual((test_repo_metadata_output_json["missing_iso3166_1_count"] + (test_repo_metadata_output_json["iso3166_1_total"])), 271, 
                "Expected the missing number of ISO 3166-1 flags and total number of flags found to add up to 271.")
        self.assertEqual((test_repo_metadata_output_json["missing_iso3166_2_count"] + (test_repo_metadata_output_json["iso3166_2_total"])), 5049,
                "Expected the missing number of ISO 3166-2 flags and total number of flags found to add up to 5,049.")
        
        #test the full repo metadata dataframe
        try:
            assert_frame_equal(test_repo_metadata.reset_index(drop=True), pd.DataFrame([test_repo_metadata_expected]).reset_index(drop=True))
        except AssertionError as e:
            self.fail(f"Expected and observed DataFrame values do not match:\n{test_repo_metadata}.")

#     @unittest.skip("")
    def test_export_flag_list(self):
        """ Testing the exporting of the ISO 3166-2 flags list. """
#1.)    
        export_flag_list(iso3166_2_flag_dir="iso3166-2-flags", export_csv_filename=os.path.join(self.test_output_dir, "test_iso3166_2_flag_list.csv"))
        test_flag_list_df = pd.read_csv(os.path.join(self.test_output_dir, "test_iso3166_2_flag_list.csv"))
        subdivisions = Subdivisions()

        self.assertEqual(len(test_flag_list_df), 5049, f"Expected 5049 rows in output CSV, got {len(test_flag_list_df)}.")                
        self.assertEqual(test_flag_list_df.columns.tolist(), ["subdivisionCode", "subdivisionName", "subdivisionType", "hasFlag", "extension", "flagChecked"], 
                f"Expected and observed output columns do not match:\n{test_flag_list_df.columns}.")
        self.assertFalse(test_flag_list_df[["subdivisionCode", "subdivisionName", "subdivisionType", "hasFlag"]].isna().any().any(),
                "Expected no null/None values in columns subdivisionCode, subdivisionName, subdivisionType, hasFlag and extension.")
        self.assertTrue(test_flag_list_df["hasFlag"].isin({"Yes", "No"}).all(), "Expected the hasFlag column to only contain the values Yes or No.")
        self.assertTrue(test_flag_list_df["extension"].dropna().isin({"SVG","PNG","JPG","JPEG"}).all(), 
                "Expected the extension column to just have the following image formats: svg, png, jpg or jpeg.")
        self.assertTrue(not (m := test_flag_list_df.duplicated(keep=False)).any(), "Expected each row to be unique.")
        self.assertTrue(test_flag_list_df["subdivisionCode"].isin([code for codes in subdivisions.subdivision_codes().values() for code in codes]).all(), 
                "Expected list of subdivision codes in column to be valid ISO 3166-2 codes.")

#     @unittest.skip("")
    def test_filter_by_size(self):
        """ Testing the filtering of the image files by file size (KB). """
#1.)
        filter_by_size(flag_dir=self.test_flag_folder, threshold=1.0, above_threshold=False, ignore_other_files=True, export_threshold_file=self.test_threshold_file)
        test_filter_by_size_df = pd.read_csv(self.test_threshold_file)
        
        self.assertEqual(list(test_filter_by_size_df.columns), ["fileName", "size (KB)"], f"Expected and observed output columns do not match:\n{test_filter_by_size_df.columns}.")
        self.assertEqual(len(test_filter_by_size_df), 5, "Expected there to be 5 rows in output dataframe.")
#2.)
        filter_by_size(flag_dir=self.test_flag_folder, threshold=1.0, above_threshold=True, ignore_other_files=True, export_threshold_file=self.test_threshold_file)
        test_filter_by_size_df = pd.read_csv(self.test_threshold_file)
        
        self.assertEqual(list(test_filter_by_size_df.columns), ["fileName", "size (KB)"], f"Expected and observed output columns do not match:\n{test_filter_by_size_df.columns}.")
        self.assertEqual(len(test_filter_by_size_df), 47, "Expected there to be 47 rows in output dataframe.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    