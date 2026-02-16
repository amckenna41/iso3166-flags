from scripts.convert_images import *
import shutil
import os
from PIL import Image
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Convert_Images_Tests(unittest.TestCase):
    """
    Test suite for testing convert_images.py script that converts flag images 
    between different formats (GIF, WEBP, PNG, JPG).

    Test Cases
    ==========
    test_convert_single_gif_to_png:
        testing conversion of single GIF file to PNG.
    test_convert_single_webp_to_png:
        testing conversion of single WEBP file to PNG.
    test_convert_directory_to_png:
        testing conversion of all images in directory to PNG.
    test_convert_nested_directory_to_png:
        testing conversion of images in nested directory structure.
    test_convert_to_jpg:
        testing conversion to JPG format.
    test_archive_functionality:
        testing archive folder creation and file archiving.
    test_delete_original_option:
        testing delete original file functionality.
    test_invalid_format_error:
        testing error handling for invalid format.
    test_missing_file_error:
        testing error handling for missing file.
    test_missing_folder_error:
        testing error handling for missing folder.
    test_invalid_file_type_error:
        testing error handling for invalid file types (skip SVG, PNG, etc).
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_flags_dir = os.path.join(self.test_output_dir, "test_convert_flags")
        self.test_nested_dir = os.path.join(self.test_flags_dir, "nested")
        self.test_archive_dir = os.path.join(self.test_output_dir, "test_archive")
        
        #create test directories
        for dir_path in [self.test_output_dir, self.test_flags_dir, self.test_nested_dir]:
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

    def create_test_image(self, filepath: str, format: str, size: tuple = (100, 150)) -> None:
        """Helper method to create test images in various formats."""
        img = Image.new('RGB', size, color='red')
        img.save(filepath, format)

    # @unittest.skip("")
    def test_convert_single_gif_to_png(self):
        """ Testing conversion of single GIF file to PNG. """
        test_gif_path = os.path.join(self.test_flags_dir, "test_flag.gif")
        test_png_path = os.path.join(self.test_flags_dir, "test_flag.png")
        
        #create test GIF file
        self.create_test_image(test_gif_path, 'GIF')
#1.)
        self.assertTrue(os.path.isfile(test_gif_path), "Test GIF file should exist.")
        
        #convert GIF to PNG
        convert_img(flag_folder=self.test_flags_dir, img_filepath=test_gif_path, img_format="png", delete_original=False)
#2.)        
        self.assertTrue(os.path.isfile(test_png_path), "Converted PNG file should exist.")
        
        #verify PNG is valid
        with Image.open(test_png_path) as img:
            self.assertEqual(img.format, 'PNG', "Output should be PNG format.")

    # @unittest.skip("")
    def test_convert_single_webp_to_png(self):
        """ Testing conversion of single WEBP file to PNG. """
        test_webp_path = os.path.join(self.test_flags_dir, "test_flag.webp")
        test_png_path = os.path.join(self.test_flags_dir, "test_flag.png")
        
        #create test WEBP file
        self.create_test_image(test_webp_path, 'WEBP')
#1.)
        self.assertTrue(os.path.isfile(test_webp_path), "Test WEBP file should exist.")
        
        #convert WEBP to PNG
        convert_img(flag_folder=self.test_flags_dir, img_filepath=test_webp_path, img_format="png", delete_original=False)
#2.)        
        self.assertTrue(os.path.isfile(test_png_path), "Converted PNG file should exist.")

    # @unittest.skip("")
    def test_convert_directory_to_png(self):
        """ Testing conversion of all images in directory to PNG. """
        #create multiple test files
        test_files = ["flag1.gif", "flag2.gif", "flag3.webp"]
        for filename in test_files:
            file_path = os.path.join(self.test_flags_dir, filename)
            format_type = 'GIF' if filename.endswith('.gif') else 'WEBP'
            self.create_test_image(file_path, format_type)
        
        #convert all files in directory
        convert_img(flag_folder=self.test_flags_dir, img_format="png", delete_original=False)
        
        #verify all files converted
        expected_pngs = ["flag1.png", "flag2.png", "flag3.png"]
        for png_file in expected_pngs:
            png_path = os.path.join(self.test_flags_dir, png_file)
            self.assertTrue(os.path.isfile(png_path), f"{png_file} should exist after conversion.")

    # @unittest.skip("")
    def test_convert_nested_directory_to_png(self):
        """ Testing conversion of images in nested directory structure. """
        #create test files in nested directory
        nested_gif_path = os.path.join(self.test_nested_dir, "nested_flag.gif")
        self.create_test_image(nested_gif_path, 'GIF')
        
        #convert nested directory
        convert_img(flag_folder=self.test_flags_dir, img_format="png", delete_original=False)
        
        #verify nested file converted
        nested_png_path = os.path.join(self.test_nested_dir, "nested_flag.png")
        self.assertTrue(os.path.isfile(nested_png_path), "Nested PNG file should exist after conversion.")

    # @unittest.skip("")
    def test_convert_to_jpg(self):
        """ Testing conversion to JPG format. """
        test_gif_path = os.path.join(self.test_flags_dir, "test_jpg.gif")
        test_jpg_path = os.path.join(self.test_flags_dir, "test_jpg.jpg")
        
        self.create_test_image(test_gif_path, 'GIF')
        
        #convert to JPG
        convert_img(flag_folder=self.test_flags_dir, img_filepath=test_gif_path, img_format="jpg", delete_original=False)
#1.)        
        self.assertTrue(os.path.isfile(test_jpg_path), "Converted JPG file should exist.")
        
        #verify JPG is valid
        with Image.open(test_jpg_path) as img:
            self.assertEqual(img.format, 'JPEG', "Output should be JPEG format.")

    # @unittest.skip("")
    def test_archive_functionality(self):
        """ Testing archive folder creation and file archiving. """
        test_gif_path = os.path.join(self.test_flags_dir, "archive_test.gif")
        self.create_test_image(test_gif_path, 'GIF')
        
        #convert with archive
        convert_img(flag_folder=self.test_flags_dir, archive_folder=self.test_archive_dir, 
                   img_filepath=test_gif_path, img_format="png", delete_original=False)
#1.)        
        self.assertTrue(os.path.isdir(self.test_archive_dir), "Archive directory should be created.")
        
        #verify original file moved to archive
        archived_file = os.path.join(self.test_archive_dir, "archive_test.gif")
        self.assertTrue(os.path.isfile(archived_file), "Original file should be in archive folder.")

    # @unittest.skip("")
    def test_delete_original_option(self):
        """ Testing delete original file functionality. """
        test_gif_path = os.path.join(self.test_flags_dir, "delete_test.gif")
        self.create_test_image(test_gif_path, 'GIF')
        
        #convert with delete option (no archive)
        convert_img(flag_folder=self.test_flags_dir, img_filepath=test_gif_path, 
                   img_format="png", delete_original=True)
#1.)        
        self.assertFalse(os.path.isfile(test_gif_path), "Original file should be deleted.")
        
        #verify PNG exists
        png_path = os.path.join(self.test_flags_dir, "delete_test.png")
        self.assertTrue(os.path.isfile(png_path), "Converted PNG should exist.")

    # @unittest.skip("")
    def test_invalid_format_error(self):
        """ Testing error handling for invalid format. """
#1.)        
        with self.assertRaises(ValueError) as context:
            convert_img(flag_folder=self.test_flags_dir, img_format="bmp")
        
        self.assertIn("Input image format not a supported format", str(context.exception))

    # @unittest.skip("")
    def test_missing_file_error(self):
        """ Testing error handling for missing file. """
        non_existent_file = os.path.join(self.test_flags_dir, "non_existent.gif")
#1.)        
        with self.assertRaises(OSError) as context:
            convert_img(flag_folder=self.test_flags_dir, img_filepath=non_existent_file, img_format="png")
        
        self.assertIn("File image not found", str(context.exception))

    # @unittest.skip("")
    def test_missing_folder_error(self):
        """ Testing error handling for missing folder. """
#1.)        
        with self.assertRaises(OSError) as context:
            convert_img(flag_folder="non_existent_folder", img_format="png")
        
        self.assertIn("Folder of flag images not found", str(context.exception))

    # @unittest.skip("")
    def test_invalid_file_type_error(self):
        """ Testing error handling for invalid file types (skip SVG, PNG, etc). """
        #create SVG and PNG files which should be skipped
        test_svg_path = os.path.join(self.test_flags_dir, "test.svg")
        test_png_path = os.path.join(self.test_flags_dir, "test.png")
        
        #create dummy files
        with open(test_svg_path, 'w') as f:
            f.write('<svg></svg>')
        self.create_test_image(test_png_path, 'PNG')
        
        #should not raise error, just skip these files
        try:
            convert_img(flag_folder=self.test_flags_dir, img_format="png", delete_original=False)
        except ValueError:
            self.fail("convert_img raised ValueError for valid skip files.")
#1.)        
        #SVG and PNG should still exist (not converted)
        self.assertTrue(os.path.isfile(test_svg_path), "SVG file should be skipped and remain.")
        self.assertTrue(os.path.isfile(test_png_path), "PNG file should be skipped and remain.")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        if os.path.isdir(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)
