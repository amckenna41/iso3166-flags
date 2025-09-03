from PIL import Image, UnidentifiedImageError
import os
import shutil
import argparse

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
        once the image file has been converted, delete the original.

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

    #raise error if file image to convert not found
    if (img_filepath != ""):
        output_img_path = f"{os.path.splitext(img_filepath)[0]}.{img_format}"
        if not (os.path.isfile(img_filepath)):
            raise OSError(f"File image not found: {img_filepath}.")

        #raise error if invalid file extension input
        if ((os.path.splitext(img_filepath)[1] in skip_files) or (os.path.splitext(os.path.basename(img_filepath))[0] == ".DS_Store")):
            raise ValueError(f"Invalid file type inputted: {img_filepath}.")

        #open image using PIL package, saving as the input format
        try:
            with Image.open(img_filepath) as img:
                if (img_format == "png"):
                    img.save(os.path.splitext(output_img_path, 'PNG'))
                else:
                    img.save(os.path.splitext(output_img_path, 'JPEG'))
        except (UnidentifiedImageError, IOError):
            print(f"Invalid file format or issue with opening it: {input_img_path}.")

        #move original unconverted file to the archive folder   
        if (archive_folder != ""):      
            shutil.move(img_filepath, os.path.join(archive_folder, img_filepath))
    else:
        #raise error if folder of images not found
        if not (os.path.isdir(flag_folder)):
            raise OSError(f"Folder of flag images not found: {flag_folder}.")

        #iterate over all images in folder, converting them into the specified format and archiving the original image, if applicable
        for item in os.listdir(flag_folder):
            if os.path.isdir(os.path.join(flag_folder, item)):
                for nested_item in os.listdir(os.path.join(flag_folder, item)):
                    input_img_path = os.path.join(flag_folder, item, nested_item)
                    output_img_path = os.path.splitext(input_img_path)[0] + "." + img_format

                    #skip svg, markdown, DS_Store as well as images in other supported formats
                    if ((os.path.splitext(input_img_path)[1] in skip_files) or (os.path.splitext(os.path.basename(input_img_path))[0] == ".DS_Store")):
                        continue
                
                    #open image using PIL package, saving as the input format, raise error if issue with opening file
                    try:
                        with Image.open(input_img_path) as img:
                            if img_format == "png":
                                img.save(output_img_path, 'PNG')
                            else:
                                img.save(output_img_path, 'JPEG')
                    except (UnidentifiedImageError, IOError):
                        print(f"Invalid file format or issue with opening it: {input_img_path}.")

                    #create nested directory folder in archive folder
                    if (archive_folder != ""):
                        if not (os.path.isdir(os.path.join(archive_folder, item))):
                            os.makedirs(os.path.join(archive_folder, item))

                        #move original image file to the same nested folder within archive folder
                        shutil.move(input_img_path, os.path.join(os.path.join(archive_folder, item), os.path.basename(input_img_path)))
                    
                    #delete the original image filepath, if applicable
                    if (delete_original):
                        os.remove(input_img_path)

            #if current item in the folder is not a nested dir then convert image to specified format and archive original image
            else:
                input_img_path = os.path.join(flag_folder, item)
                output_img_path = os.path.splitext(input_img_path)[0] + "." + img_format

                #skip svg, markdown, DS_Store as well as images in other supported formats
                if ((os.path.splitext(input_img_path)[1] in skip_files) or (os.path.splitext(os.path.basename(input_img_path))[0] == ".DS_Store")):
                    continue

                #open image using PIL package, saving as the input format, raise error if issue with opening file
                try:
                    with Image.open(input_img_path) as img:
                        if (img_format == "png"):
                            img.save(output_img_path, 'PNG')
                        else:
                            img.save(output_img_path, 'JPEG')
                except (UnidentifiedImageError, IOError):
                    print(f"Invalid file format or issue with opening it: {input_img_path}.")

                #move original image file to the archive folder
                if (archive_folder != ""):
                    shutil.move(input_img_path, os.path.join(archive_folder, os.path.basename(input_img_path)))

                #delete the original image filepath, if applicable
                if (delete_original):
                    os.remove(input_img_path)

if __name__ == "__main__":

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-flag_folder', '--flag_folder', type=str, required=False, default="iso3166-2-flags-edit-this-one", 
        help='Input folder of ISO 3166 flags to convert to specified format.')
    parser.add_argument('-archive_folder', '--archive_folder', type=str, required=False, default="flag_icon_conversion_archive", 
        help='Archive folder that maintains the original unconverted ISO 3166 flags.')
    parser.add_argument('-img_file_path', '--img_file_path', type=str, required=False, default="", 
        help='Filepath to individual image to convert. The file will take precedence over a folder of images input.')
    parser.add_argument('-img_format', '--img_format', type=str, required=False, default="png", 
        help='File format to convert the images into, accepted formats are png, jpg or jpeg (png by default).')
    parser.add_argument('-delete_original', '--delete_original', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Set to 1 to delete the original image file once converted, by default it is kept.')
    
    #parse input args
    args = parser.parse_args()

    #call main conversion function
    convert_img(**vars(args))