from PIL import Image, UnidentifiedImageError
import os
import shutil
import argparse
import warnings

#suppress libpng iCCP warnings
warnings.filterwarnings("ignore", message=".*iCCP.*", category=UserWarning)

def convert_one_img(input_img_path: str, img_format: str) -> bool:
    """
    Convert a single image file into the specified format, writing the output alongside
    the input with the new extension.

    Parameters
    ==========
    :input_img_path: str
        filepath to the image to convert.
    :img_format: str
        image format to convert into - png, jpg or jpeg.

    Returns
    =======
    :converted: bool
        True if the image was successfully converted and written, False if the file
        could not be opened or saved. Callers must not archive or delete the original
        unless this returns True.
    """
    output_img_path = os.path.splitext(input_img_path)[0] + "." + img_format
    try:
        with Image.open(input_img_path) as img:
            #convert to RGB if necessary for JPEG
            if img_format in ["jpg", "jpeg"] and img.mode in ('P', 'RGBA', 'LA'):
                img = img.convert('RGB')

            img.save(output_img_path, 'PNG' if img_format == "png" else 'JPEG')
        return True
    except (UnidentifiedImageError, IOError, OSError, ValueError) as e:
        print(f"Invalid file format or issue with opening it: {input_img_path} ({e}).")
        return False

def convert_img(flag_folder: str, archive_folder: str="", img_filepath: str="", img_format="png", delete_original: bool=False) -> None:
    """
    Convert any flag images in the GIF or WEBP format into a specified format (png by default). 
    The function can accept a folder to iterate through, converting all GIFs/WEBPs, or it can 
    accept a single filepath for an image. Additionally, an optional archive folder can be set 
    up such that the original GIF/WEBP files are maintained (non-converted images are not 
    added to this archive folder). The valid formats supported to be converted into are: 
    png, jpg & jpeg.

    Parameters
    ========== 
    :flag_folder: str
        path to directory of flag images to convert, can be a single directory
        or a nested directory like that of iso3166-2-flags.
    :archive_folder: str (default="")
        backup folder which stores the original unconverted file.
    :img_filepath: str (default="")
        filepath to single image to be converted. If this parameter is non-empty
        then it will take precedence over the folder of images.
    :img_format: str (default="png")
        image format to convert image into, e.g png, jpg & jpeg.
    :delete_original: bool (default=False)
        once the image file has been converted, delete the original. The original is only
        ever archived or deleted after a successful conversion.

    Returns
    =======
    None

    Raises
    ======
    ValueError:
        Input image format is not supported.
        Invalid image file type.
    OSError:
        Image file not found.
        Folder of images not found.
    UnidentifiedImageError:
        Invalid image file format.
    """    
    #create archives folder
    if (archive_folder != ""):
        if not (os.path.isdir(archive_folder)):
            os.makedirs(archive_folder)

    #lowercase input file format
    img_format = img_format.lower()

    #raise error if invalid image format put into the parameter
    valid_formats = ["png", "jpg", "jpeg"]
    if not (img_format in valid_formats):
        raise ValueError(f"Input image format not a supported format: {img_format}.")

    #list of file extensions to skip
    skip_files = [".png", ".svg", ".jpg", ".jpeg", ".md"]

    def archive_or_delete(input_img_path: str, relative_dir: str="") -> None:
        """
        Archive or delete the original image after a successful conversion, mirroring any
        sub-folder structure within the archive folder.
        """
        if (archive_folder != ""):
            #create the mirrored sub-folder within the archive folder, if applicable
            archive_dir = os.path.join(archive_folder, relative_dir) if relative_dir else archive_folder
            if not (os.path.isdir(archive_dir)):
                os.makedirs(archive_dir)

            #move original image file into the archive folder
            shutil.move(input_img_path, os.path.join(archive_dir, os.path.basename(input_img_path)))

        #delete the original image filepath, if applicable
        elif (delete_original):
            os.remove(input_img_path)

    #raise error if file image to convert not found
    if (img_filepath != ""):
        if not (os.path.isfile(img_filepath)):
            raise OSError(f"File image not found: {img_filepath}.")

        #raise error if invalid file extension input
        if ((os.path.splitext(img_filepath)[1] in skip_files) or (os.path.splitext(os.path.basename(img_filepath))[0] == ".DS_Store")):
            raise ValueError(f"Invalid file type inputted: {img_filepath}.")

        #only archive or delete the original once the conversion has actually succeeded, otherwise
        #a file that PIL can't decode would be lost with no converted replacement written
        if convert_one_img(img_filepath, img_format):
            archive_or_delete(img_filepath)
    else:
        #raise error if folder of images not found
        if not (os.path.isdir(flag_folder)):
            raise OSError(f"Folder of flag images not found: {flag_folder}.")

        #walk the folder recursively, handling both the flat iso3166-1-flags layout and the
        #nested iso3166-2-flags layout, converting each image into the specified format
        for folder_path, _, filenames in os.walk(flag_folder):
            #sub-folder of flag_folder the current file sits in, used to mirror the archive structure
            relative_dir = os.path.relpath(folder_path, flag_folder)
            relative_dir = "" if relative_dir == "." else relative_dir

            for filename in filenames:
                input_img_path = os.path.join(folder_path, filename)

                #skip svg, markdown, DS_Store as well as images in other supported formats
                if ((os.path.splitext(filename)[1] in skip_files) or (os.path.splitext(filename)[0] == ".DS_Store")):
                    continue

                #as above, the original is only archived or deleted after a successful conversion
                if convert_one_img(input_img_path, img_format):
                    archive_or_delete(input_img_path, relative_dir)

if __name__ == "__main__":

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for converting GIF/WEBP flag images into the png, jpg or jpeg format.')

    parser.add_argument('-flag_folder', '--flag_folder', type=str, required=False, default="iso3166-2-flags",
        help='Input folder of ISO 3166 flags to convert to specified format.')
    parser.add_argument('-archive_folder', '--archive_folder', type=str, required=False, default="flag_icon_conversion_archive",
        help='Archive folder that maintains the original unconverted ISO 3166 flags.')
    parser.add_argument('-img_filepath', '--img_filepath', type=str, required=False, default="",
        help='Filepath to individual image to convert. The file will take precedence over a folder of images input.')
    parser.add_argument('-img_format', '--img_format', type=str, required=False, default="png", 
        help='File format to convert the images into, accepted formats are png, jpg or jpeg (png by default).')
    parser.add_argument('-delete_original', '--delete_original', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to delete the original image file once converted, by default it is kept.')
    
    #parse input args
    args = parser.parse_args()

    #call main conversion function
    convert_img(**vars(args))