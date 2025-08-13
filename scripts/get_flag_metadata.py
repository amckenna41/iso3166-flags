import argparse
import os
import csv
import re
import cv2  
import iso3166
from iso3166_2 import Subdivisions
from PIL import Image, UnidentifiedImageError
from lxml import etree
import pandas as pd
import json
import xml.etree.ElementTree as ET
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="PIL") #ignore any warnings from Pillow module

def export_flag_metadata(flag_folder: str, flag_metadata_output: str="flag_metadata.csv") -> None:
    """
    Export flag image file metadata for all of the subdivision and country flags in the flag folder. The metadata per 
    image exported is: file name, file size, image dimensions, aspect ratio, flag type (normal flag, coat of arms, 
    banner or seal) and image quality/blurriness ratio.

    Parameters
    ========= 
    :flag_folder: str
        file path to folder of flags.
    :flag_metadata_output: str
        output file name for metadata csv.
    
    Returns
    ====== 
    None

    Raises
    ======
    OSError:
        Flag folder not found.
    """
    #raise error if folder of images not found
    if not (os.path.isdir(flag_folder)):
        raise OSError(f"Folder of subdivision flag images not found: {flag_folder}.")
    
    #var to delinate whether iso3166-1-icons or iso3166-2-icons folder is being used to determine 1st column
    if (flag_folder == "iso3166-1-icons"):
        country_subdivision_code = "country_code"
    else:
        country_subdivision_code = "subdivision_code"        

    #get list of columns in csv output - first column can be country_code or subdivision_code
    attribute_list = [country_subdivision_code, 'file_name', 'file_size_kb', 'file_extension', 'dimensions', 'aspect_ratio', 'flag_type', 'quality']

    #list of each row
    file_info_list = []

    #tuple of valid flag extensions
    valid_exts = ('.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp')
    
    #iterate over the folder recursively (handles flat [iso3166-1-icons] and nested layouts [iso3166-2-icons])
    for root, _, files in os.walk(flag_folder):
        for file_name in files:
            #skip hidden files and macOS resource forks
            if file_name.startswith('.') or file_name.startswith('._'):
                continue
            #get the metadata for the current file at iteration
            if file_name.lower().endswith(valid_exts):
                file_info = get_file_info(os.path.join(root, file_name))
                file_info[country_subdivision_code] = file_info["subdivision_code"]
                #for country flags remove the subdivision code attribute
                if (file_info.get("country_code") is not None):
                    del file_info["subdivision_code"]
                file_info_list.append(file_info)

    #sort rows alphabetically, depending on flag folder
    file_info_list.sort(key=lambda x: x[country_subdivision_code])

    #open csv file for storing metadata export
    with open(flag_metadata_output, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=attribute_list)
        writer.writeheader()
        for file_info in file_info_list:
            writer.writerow(file_info)

def calculate_dimension(image_path: str) -> tuple[int, int]:
    """
    Calculate the dimensions of the image, getting its
    height, width and aspect ratio.

    Parameters
    ==========
    :image_path: str
        file path to image
    
    Returns
    =======
    :width: int
        width of image.
    :height: int
        height of image.
    :aspect_ratio: float
        aspect ratio of image.

    Raises
    ====== 
    FileNotFoundError:
        Image file not found on path.
    UnidentifiedImageError:
        Invalid image.
    IOError:
        Error reading image.
    """
    #if input image file is a SVG, raise error, calculate_svg_dimension function should be used
    if (os.path.splitext(image_path)[1] == ".svg"):
        raise ValueError("For SVG files, please use the calculate_svg_dimensions function.")

    #try and parse input image file, calculating its dimension (height/width) & aspect ratio using Image
    try:
        with Image.open(image_path) as img:
            width, height = img.size 
            aspect_ratio = round(width / height, 2)
            return width, height, aspect_ratio
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        raise
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {image_path}")
        raise
    except IOError:
        print(f"Error reading the image file: {image_path}")
        raise
    
def calculate_quality(image_path):
    """ 
    Calculate the quality/blurriness of the image using Laplacian 
    variance in CV2 library. In this metric, a higher value means
    less blurry, thus higher quality - vice versa.

    Parameters
    ==========
    :image_path: str
        file path to image.

    Returns
    =======
    :image_quality: float
        quality of image as a %, higher value means higher quality,
        vice versa.

    Raises
    ====== 
    FileNotFoundError:
        Image file not found on path.
    IOError:
        Error reading image.
    """
    #raise error if filepath not found 
    if not (os.path.isfile(image_path)):
        raise FileNotFoundError(f"Could not find image at path: {image_path}.")

    #read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    #raise error if error reading file
    if (image is None):
        raise IOError(f"Could not read image at path: {image_path}.")

    #compute the Laplacian variance (higher means less blurry)
    blurriness = cv2.Laplacian(image, cv2.CV_64F).var()

    #normalize quality based on file size and blurriness
    quality = min(100, blurriness / 100 * 2) 

    return round(quality, 2)

def calculate_svg_quality(svg_path):
    """
    Calculate a quality score for an SVG file based on its complexity. 
    This requires a different process than png and jpeg files. The quality
    number output is a proxy metric based on number of vector elements.

    SVGs are vector graphics so there's no concept of blurriness as no 
    pixels. The funtion counts the total number of a range of SVG drawing
    elements, more elements usually means more detail & higher visual 
    quality.

    Parameters
    ==========
    :svg_path: str
        path to the SVG file.

    Returns
    =======
    :quality: float
        Estimated quality score from 0–100 based on SVG complexity.

    Raises
    ======
    FileNotFoundError:
        If the SVG file is not found.
    ET.ParseError:
        If the file is not a valid SVG/XML.
    """
    if not os.path.isfile(svg_path):
        raise FileNotFoundError(f"SVG not found at: {svg_path}")

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        #each SVG should have a namepsace at the top as they are XML
        namespace = {'svg': 'http://www.w3.org/2000/svg'}
        ET.register_namespace('', namespace['svg'])

        #get count of common vector elements
        elements = ['path', 'rect', 'circle', 'line', 'polygon', 'polyline', 'ellipse']
        count = sum(len(root.findall(f".//svg:{el}", namespace)) for el in elements)

        #normalize to 0–100 scale
        quality = min(100, count * 2)  #50 elements = 100 quality
        return round(quality, 2)

    #raise ElementTree parsing error
    except ET.ParseError:
        raise ET.ParseError(f"Could not parse SVG at: {svg_path}.")

def get_file_info(image_file_path: str) -> dict:
    """
    Gather the individual image info/metadata.    

    Parameters
    ==========
    :image_file_path: str
        image file path.

    Returns
    =======
    :file_info: dict
        object of calculated subdivision flag file metadata. 
    """
    #raise error if invalid filepath
    if not (os.path.isfile(image_file_path)):
        raise OSError(f"Image file not found on path: {image_file_path}.")

    #get subdivision code from filename, get path to image
    subdivision_code = os.path.basename(os.path.splitext(image_file_path)[0])

    #get file size in bytes - used for calculating image quality, also get file size in KB, round to 3.dp
    # file_size = os.path.getsize(image_file_path)  #bytes
    file_size_kb = round((os.path.getsize(image_file_path) / 1024), 3)

    #get file extension
    file_extension = os.path.splitext(image_file_path)[1].replace('.', '') 

    #get image dimensions, call specific svg function to get svg dimensions
    if (file_extension == 'svg'):
        width, height, aspect_ratio = calculate_svg_dimension(image_file_path)
    else:
        width, height, aspect_ratio = calculate_dimension(image_file_path)

    #create tuple of dimensions
    dimensions = (height, width)

    #calculate image quality/blurriness - set to NA for SVGs
    if (file_extension == 'svg'):
        quality = calculate_svg_quality(image_file_path)
        # quality = "NA"
    else:
        quality = calculate_quality(image_file_path)

    return {
        'subdivision_code': subdivision_code,
        'file_name': os.path.basename(image_file_path),
        'file_size_kb': file_size_kb,
        'file_extension': file_extension.upper(),
        'dimensions': dimensions,
        'aspect_ratio': aspect_ratio,
        'flag_type': None,
        'quality': quality
    }

def calculate_svg_dimension(svg_file_path: str) -> tuple:
    """
    Get the file metadata for SVG images which cannot be parsed
    or imported via the PIL package. 

    Parameters
    ==========
    :svg_file_path: str
        path to SVG image file.
    
    Returns
    =======
    :width: float
        width of SVG.
    :height: float
        height of SVG.
    :aspect_ratio: float
        aspect ratio of SVG.
    
    Raises
    ======
    OSError: 
        Image file cannot be found on path.
    """
    #raise error if invalid filepath
    if not (os.path.isfile(svg_file_path)):
        raise OSError(f"Image file not found on path: {svg_file_path}.")
    
    try:
        #traverse svg object data, getting the dimensions
        tree = etree.parse(svg_file_path)
        root = tree.getroot()
        width = root.get("width")
        height = root.get("height")

        #parse the dimension from the SVG file - converting float values into pixels
        width = parse_svg_dimension(width)
        height = parse_svg_dimension(height)

        #if width and height are not defined, try to extract from the viewBox
        if width is None or height is None:
            view_box = root.get("viewBox")
            if view_box:
                _, _, width, height = map(float, view_box.split())

        #if width or height is missing, extract from viewBox attribute
        if width is not None and height is not None:
            width = round(float(width))
            height = round(float(height))
            aspect_ratio = round(width / height, 2)
            return width, height, aspect_ratio #aspect_ratio, 'SVG', (72, 72)  # Default DPI for SVG
        else:
            print(f"Unable to determine dimensions for SVG file: {svg_file_path}.")
            return None, None, None # None, 'SVG', (72, 72)
    except Exception as e:
        print(f"Error parsing SVG file {svg_file_path}: {e}")
        return None, None, None # None, 'SVG', (72, 72)

def parse_svg_dimension(dimension: str):
    """
    Convert dimension strings in an image into pixel-based float values, 
    e.g 100px, 5cm, 1.5in etc. Percentage based dimension units are 
    not supported as they are relative, not absolute. 
    
    Parameters
    ==========
    :dimension: str
        dimension string of SVG.
    
    Returns
    =======
    :value: float
        pixel-based float conversion of SVG dimension string.
    
    Raises
    ======
    IOError:
        Error converting SVG file dimension to float.
    ValueError:
        Percentage based dimension unit input for SVG which is not supported.
    """
    #return None if input is None
    if dimension is None:
        return None
    try:
        #remove any non-numeric characters (like 'px', 'mm', etc.), extracting numeric part and unit
        match = re.match(r"([0-9.]+)([a-zA-Z%]*)", dimension)
        if match:
            value, unit = match.groups()
            value = float(value)
            
            #handle different units if necessary (default to px)
            if unit == 'mm':
                value *= 3.7795275591  #convert mm to pixels (1 mm = ~3.78 px)
            elif unit == 'cm':
                value *= 37.795275591  #convert cm to pixels
            elif unit == 'in':
                value *= 96  #convert inches to pixels (1 in = 96 px)
            elif unit == 'pt':
                value *= 1.333333  #1pt = 1/72 inch, and 1in = 96px
            elif unit == 'pc':
                value *= 16  #1pc = 12pt = 16px
            elif unit == '%':
                raise ValueError(f"Percentage-based dimensions '{dimension}' are not supported.")
            
            #round value to 3 d.p
            value = round(value, 3)

            return value
        else:
            print(f"Unable to parse dimension: {dimension}")
            return None
    except IOError:
        print(f"Error converting dimension to float: {dimension}")
        return None

def export_repo_metadata(export_json: bool=True, export_filename: str="repo_metadata", exclude_readme: bool=True) -> pd.Series: 
    """ 
    Function that returns a plethora of useful data and info about the repository of flags
    that is added to the main README file. These include the total number of flags, total 
    number of flags per format (the supported formats are svg, png, jpeg and jp), size of
    repo, average file size, size of flag folders, and count of countrues/subdivisions 
    that don't have a supported flag. The function also counts the total number of 
    files and duplicates, returning the name of any duplicate subdivisions.

    By default, the metadata will be exported for the iso3166-1-icons and iso3166-2-icons
    directories.

    Parameters
    ==========
    :export_json: bool (default=True)
        export the output object of image counts to JSON.
    :export_filename: str (default="file_format_count")
        filename for export.
    :exclude_readme: bool (default=True)
        exclude each subdivision folder's markdown file in the overall repo size 
        calculation.

    Returns
    =======
    :flag_metadata_df: pd.Series
        dataframe of all repository metadata and attributes.

    Raises
    ======
    OSError:
        Folder of flags not found.
    """
    #object holding metadata for repo
    flag_metadata_master = {
        "total": 0, "iso3166_1_total": 0, "iso3166_2_total": 0, "svg": 0, "png": 0, "jpg/jpeg": 0,  
        "other": 0, "duplicates": 0, "subdivisions_other": [], "duplicate_list": [], "total_repo_size": 0, 
        "iso3166_1_flags_size": 0, "iso3166_2_flags_size": 0, "average_flag_size": 0
    }
    #flag directory names
    iso3166_1_dir = "iso3166-1-icons"
    iso3166_2_dir = "iso3166-2-icons"

    #list of valid flag extensions 
    valid_exts = ['.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp']
    
    def get_directory_metadata(path: str) -> dict:
        """ 
        Auxillary function that exports the metadata per input folder. This function is called 
        for each of the iso3166-1-icons and iso3166-2-icons directories. 

        Parameters
        ==========
        :path: str
            path to the flag directory.

        Returns
        =======
        :flag_metadata: dict
            object holding all of the directory metadata.
        """
        all_files = []          #stores filename - no extension
        total_size_bytes = 0    #total size of all files in bytes

        #initialised object of all folder metadata
        flag_metadata = {
            "total": 0, "svg": 0, "png": 0, "jpg/jpeg": 0, "other": 0, "duplicates": 0, 
            "subdivisions_other": [], "duplicate_list": [], "total_folder_size": 0}

        #iterate over all files in folder, get its metadata, size, duplicates, keep track of total & total per ext
        for folder_path, sub_folders, filenames in os.walk(path):
            
            #iterate over the filenames in the current folder
            for filename in filenames:
                #extract filename and extension
                name, ext = os.path.splitext(filename)

                #skip markdown & DS_Store files, if exclude_readme set to False then include in count
                if (exclude_readme):
                    if (ext == ".md" or name == ".DS_Store"):
                        continue
        
                #get full filepath to flag
                fpath = os.path.join(folder_path, filename)
                
                #increment file type counter and append to object
                if (ext == '.svg'):
                    flag_metadata["svg"] += 1
                elif (ext == '.png'):
                    flag_metadata["png"] += 1
                elif (ext == '.jpg' or ext == '.jpeg'):
                    flag_metadata["jpg/jpeg"] += 1
                else:
                    if (exclude_readme):
                        flag_metadata["other"] += 1
                        flag_metadata["subdivisions_other"].append(filename)    

                #increment total file counter, don't include readme in total regardless if parameter is set
                if not (ext == ".md" or name == ".DS_Store"):
                    flag_metadata["total"] += 1
                
                #add subdivision name to duplicate list and increment counter, if applicable, skip over markdown files
                if not (ext == ".md" or name == ".DS_Store"):
                    if (name in all_files):
                        flag_metadata["duplicate_list"].append(name)
                        flag_metadata["duplicates"] += 1
                    else:
                        all_files.append(name)

                #get the individual file sizes
                if ext in valid_exts:
                    #use the os.path module to get the current file size
                    try:
                        file_sizes = os.path.getsize(fpath)
                    except OSError(f"Error getting size of file: {fpath}"):
                        file_sizes = 0
                    #append individual file size to total var
                    total_size_bytes += file_sizes

        #set the total directory size
        flag_metadata["total_folder_size"] = total_size_bytes

        return flag_metadata

    #total number of flag across the 2 directories
    total_flag_count = 0

    #get the metadata for the iso3166-1-icons flag
    flag_metadata_iso3166_1 = get_directory_metadata(iso3166_1_dir)

    #set the total number of flags & total size (in bytes)
    flag_metadata_master["iso3166_1_total"] = flag_metadata_iso3166_1["total"]
    flag_metadata_master["iso3166_1_flags_size"] = flag_metadata_iso3166_1["total_folder_size"] 

    #increment the total flags counter
    total_flag_count += flag_metadata_master["iso3166_1_total"]

    #get the metadata for the iso3166-2-icons flag
    flag_metadata_iso3166_2 = get_directory_metadata(iso3166_2_dir)

    #set the total number of flags & total size (in bytes)
    flag_metadata_master["iso3166_2_total"] = flag_metadata_iso3166_2["total"]
    flag_metadata_master["iso3166_2_flags_size"] = flag_metadata_iso3166_2["total_folder_size"] 

    #increment the total flags counter
    total_flag_count += flag_metadata_master["iso3166_2_total"]

    #update the attribute values for the master object across the 2 directories
    flag_metadata_master["total"] = flag_metadata_iso3166_1["total"] + flag_metadata_iso3166_2["total"]
    flag_metadata_master["svg"] = flag_metadata_iso3166_1["svg"] + flag_metadata_iso3166_2["svg"]
    flag_metadata_master["png"] = flag_metadata_iso3166_1["png"] + flag_metadata_iso3166_2["png"]
    flag_metadata_master["jpg/jpeg"] = flag_metadata_iso3166_1["jpg/jpeg"] + flag_metadata_iso3166_2["jpg/jpeg"]
    flag_metadata_master["other"] = flag_metadata_iso3166_1["other"] + flag_metadata_iso3166_2["other"]
    flag_metadata_master["duplicates"] = flag_metadata_iso3166_1["duplicates"] + flag_metadata_iso3166_2["duplicates"]
    flag_metadata_master["subdivisions_other"] = flag_metadata_iso3166_1["subdivisions_other"] + flag_metadata_iso3166_2["subdivisions_other"]
    flag_metadata_master["duplicate_list"] = flag_metadata_iso3166_1["duplicate_list"] + flag_metadata_iso3166_2["duplicate_list"]

    #get the total size (in bytes) for the 2 flag directories
    flag_metadata_master["total_repo_size"] = flag_metadata_master["iso3166_1_flags_size"] + flag_metadata_master["iso3166_2_flags_size"]

    #convert all the folder size attributes to KB, round to 3d.p
    flag_metadata_master["iso3166_1_flags_size"] = f"{round(flag_metadata_master['iso3166_1_flags_size'] / 1024, 3):,.3f}KB"
    flag_metadata_master["iso3166_2_flags_size"] = f"{round(flag_metadata_master['iso3166_2_flags_size'] / 1024, 3):,.3f}KB"
    flag_metadata_master["average_flag_size"] = f"{round(flag_metadata_master['total_repo_size'] / total_flag_count, 3):,.3f}KB"
    flag_metadata_master["total_repo_size"] = f"{round(flag_metadata_master['total_repo_size'] / 1024, 3):,.3f}KB"

    ### Get list of any missing ISO 3166-1 flags not in flag directory ###

    #get list of official iso3166-1 coutry codes
    missing_iso3166_1_count = 0
    all_country_codes = [f.lower() for f in list(iso3166.countries_by_alpha2.keys())]

    #list of country codes found as flags in folder
    country_codes_found = []

    #iterate over all flags, compare list of flags with that of the official list
    if os.path.isdir(iso3166_1_dir):
        for f in os.listdir(iso3166_1_dir):
            filename, ext = os.path.splitext(f)
            if ext.lower() in valid_exts:
                country_codes_found.append(filename.lower())
        #get list of missing country codes with no supported flags
        missing_iso3166_1_count = len(set(all_country_codes) - set(country_codes_found))

    #set count of missing ISO 3166-1 flags
    flag_metadata_master["missing_iso3166_1_count"] = missing_iso3166_1_count

    ### Get list of any missing ISO 3166-2 flags not in flag directory ###

    #get list of official iso3166-2 subdivision codes
    missing_iso3166_2_count = 0
    subdivsions = Subdivisions()

    #list of subdivision codes found as flags in folder
    subdivision_codes_found = []

    #get flattened list of all subdivision codes
    all_subdivision_codes = subdivsions.subdivision_codes()
    all_subdivision_codes = [subd for subdivisions in all_subdivision_codes.values() for subd in subdivisions] 

    #iterate over all flags, compare list of flags with that of the official list
    if os.path.isdir(iso3166_2_dir):
        for root, _, files in os.walk(iso3166_2_dir):
            for f in files:
                filename, ext = os.path.splitext(f)
                if ext.lower() in valid_exts:
                    subdivision_codes_found.append(filename)
        #get list of missing subdivision codes with no supported flags
        missing_iso3166_2_count = len(set(all_subdivision_codes) - set(subdivision_codes_found))
        
    #set count of missing ISO 3166-2 flags
    flag_metadata_master["missing_iso3166_2_count"] = missing_iso3166_2_count

    #convert dict into pandas series
    file_metadata_df = pd.DataFrame([flag_metadata_master])
    
    #export to json
    if (export_json):
        if (os.path.splitext(export_filename)[1] != ".json"):
            export_filename = os.path.splitext(export_filename)[0] + ".json"
        with open(export_filename, 'w', encoding='utf-8') as f:
            json.dump(flag_metadata_master, f, ensure_ascii=False, indent=4)

    return file_metadata_df

    #** create plot:
    # #generate bar chart
    # format_counts = [flag_metadata["svg"], flag_metadata["png"], flag_metadata["jpg/jpeg"], flag_metadata["jpeg"], flag_metadata["other"]]
    # labels = ["SVG", "PNG", "JPG", "JPEG", "GIF", "WEBP", "Other"]

    # plt.bar(labels, format_counts)
    # plt.xlabel("Image Formats")
    # plt.ylabel("Counts")
    # plt.title("Image Format Distribution")
    # plt.savefig("image_format_distribution.png")
    #     #rejig the width/height values 
    #     if width is not None and height is not None:
    #         width = float(width.replace("px", ""))  
    #         height = float(height.replace("px", ""))
    #         # aspect_ratio = round(width / height, 2)
    #         return width, height # 'SVG', (72, 72)  # SVG doesn't have DPI, so use defaults ***
    # except Exception as e:
    #     print(f"Error parsing SVG file: {e}")
    #     return None, None

import os
import csv

def export_flag_list(iso3166_2_flag_dir: str="iso3166-2-icons", export_csv_filename: str="iso3166_2_flag_list.csv",) -> None:
    """
    Export the full list of ISO 3166-2 subdivision codes and names (via iso3166-2),
    plus whether a flag file currently exists in iso3166-2-icons. The output CSV
    will include the columns: subdivisionCode, subdivisionName, hasFlag, flagChecked.

    Parameters
    ==========
    :iso3166_2_flag_dir: str (default="iso3166-2-icons)
        flag icons folder.
    :export_csv_filename: str (default="iso3166_2_flag_list.csv")
        filename for ouptu csv.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Flag folder not found.
    """ 
    #raise error if flag folder not found
    if not os.path.isdir(iso3166_2_flag_dir):
        raise OSError(f"Folder not found: {iso3166_2_flag_dir}")

    #list of subdivision flags in folder
    subdivision_flags_list = []

    #iterate over flag folder, add flag filename to above list
    for root, _, files in os.walk(iso3166_2_flag_dir):
        for filename in files:
            #ignore hidden/AppleDouble junk
            if filename.startswith(".") or filename.startswith("._"):
                continue
            name, ext = os.path.splitext(filename)
            #dont include markdown or ds_store files
            if (ext.lower() == ".md" or ext.lower() == ".ds_store"):
                continue
            else:
                #add flag name to list
                subdivision_flags_list.append(name.upper())

    #create instance of Subdivisions class, get list of all official codes
    subdivisions = Subdivisions()
    all_subdivision_codes = subdivisions.subdivision_codes()
  
    #iterate over all official subdiv codes, append row to output csv_rows if subdiv has corresponding flag file
    csv_rows = []
    for country_code, subdiv_list in all_subdivision_codes.items():
        for subdiv_code in subdiv_list:
            subdiv_name = subdivisions[country_code][subdiv_code]["name"]
            has_flag = "Yes" if subdiv_code in subdivision_flags_list else "No"
            csv_rows.append({
                "subdivisionCode": subdiv_code,
                "subdivisionName": subdiv_name,
                "hasFlag": has_flag,
                "flagChecked": None
            })

    #write object to CSV
    with open(export_csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["subdivisionCode", "subdivisionName", "hasFlag", "flagChecked"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"Exported {len(csv_rows)} subdivisions to {export_csv_filename}.")

if __name__ == '__main__':
    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting various metadata per iso3166-2 subdivision flag.')

    parser.add_argument('-flag_folder', '--flag_folder', type=str, required=False, default="iso3166-1-icons", 
        help='Path to flag folder (iso3166-1-icons or iso3166-2-icons).')
    parser.add_argument('-flag_metadata_output', '--flag_metadata_output', type=str, required=False, default="subdivision_flag_metadata.csv", 
        help='Output file name/path for subdivision flag metadata export.')
    parser.add_argument('-export_json', '--export_json', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to export the metadata output to json.')
    parser.add_argument('-exclude_readme', '--exclude_readme', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Set to 1 to exclude the country markdown files in the overall file count and metadata calculation.')
    
    #parse input args
    args = parser.parse_args()
    flag_folder = args.flag_folder
    flag_metadata_output = args.flag_metadata_output
    export_json = args.export_json
    exclude_readme = args.exclude_readme

    #call main export function
    export_flag_metadata(flag_folder, flag_metadata_output=flag_metadata_output)