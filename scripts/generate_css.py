import os 
import argparse

def create_iso3166_1_css(country_input_folder: str="iso3166-1-flags", export_css_filepath: str="iso3166-1-flags.css") -> None:
    """
    Create custom CSS file for all ISO 3166-1 flags. Each flag will have its own custom CSS 
    selector that is linked to the filepath of the flag within the repo, for example: ".fi-al", ".fi-vn"
    and ".fi-za" are the class selectors for Albania, Vietnam & South Africa, respectively. Within 
    each of these selectors, the background-image attribute will be used with a relative link to the
    flag on the repo.

    Parameters
    ==========
    :country_input_folder: string (default="iso3166-1-flags")
        folder where ISO 3166-1 flags are stored on repo.
    :export_css_filepath: str (default="iso3166-1-flags.css")
        export filename for generated ISO 3166-1 CSS file.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-1 country flags not found.
    """
    #initial css attributes and selector data
    css_output_str = ".fib { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n} \
                \n\n.fi { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n\tposition: relative; \
                \n\tdisplay: inline-block; \n\twidth: 1.33333333em; \n\tline-height: 1em; \n} \
                \n\n.fi.fis { \n\twidth: 1em; \n}\n"
                # \n.fi:before { \ncontent: '\00a0'; \n} \n.fi.fis { \nwidth: 1em; \n}"

    #create css file, append the initial required CSS selectors and attributes
    with open(export_css_filepath, "w") as css_file:
        css_file.write(css_output_str)
    
    #raise error if folder of ISO 3166-1 flags not present
    if not (os.path.isdir(country_input_folder)):
        raise OSError(f"Folder of ISO 3166-1 country flags not found: {country_input_folder}.")

    #get list of all ISO 3166-1 flag svg files
    all_files = [f for f in os.listdir(country_input_folder) if os.path.isfile(os.path.join(country_input_folder, f))]

    #iterate through all flag files, creating a custom and unique CSS class selector for each 
    for code in all_files:
        css_output_str += "\n.fi-" + os.path.splitext(code)[0] + " {\n" + "\tbackground-image: url(" + country_input_folder + "/" + code + ");\n}\n"

    #append output string to CSS file
    with open(export_css_filepath, "a") as css_file:
        css_file.write(css_output_str)

def create_iso3166_2_css(country_input_folder: str="iso3166-2-flags", export_css_filepath: str="iso3166-2-flags.css") -> None:
    """
    Create custom CSS file for all ISO 3166-2 flags. Each subdivision flag will have its own custom 
    CSS selector that is linked to the filepath of the flag, for example: ".fi-us-us-tx", ".fi-ga-ga-1" 
    and ".fi-lu-ca" are the CSS class selectors for the US State of Texas (US-TX), the Gabonese province of 
    Estuaire (GA-1) and the Luxembourgish canton of Capellen (LU-CA), respectively. Within each of these 
    selectors, the background-image attribute will be used with a relative link to the flag on the repo.

    Parameters
    ==========
    :country_input_folder: string (default="iso3166-2-flags")
        filename of folder for where ISO 3166-2 flags are stored.
    :export_css_filepath: str (default="iso3166-2-flags.css")
        export folder for generated ISO 3166-2 CSS file.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-2 subdivision flags not found.
    """
    #initial css attributes and selector data
    css_output_str = ".fib { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n} \
                \n.fi { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n\tposition: relative; \
                \n\tdisplay: inline-block; \n\twidth: 1.33333333em; \n\tline-height: 1em; \n} \
                \n.fi.fis { \n\twidth: 1em; \n}\n"
                # \n.fi:before { \ncontent: '\00a0'; \n} \n.fi.fis { \nwidth: 1em; \n}"
                
    #create css file, append the initial required CSS selectors and attributes
    with open(export_css_filepath, "w") as css_file:
        css_file.write(css_output_str)

    #raise error if folder of ISO 3166-2 flags not present
    if not (os.path.isdir(country_input_folder)):
        raise OSError(f"Folder of ISO 3166-2 country flags not found: {country_input_folder}.")
    
    #get list of all country sub-folders in ISO 3166-2 folder
    all_folders = sorted([f for f in os.listdir(country_input_folder) if os.path.isdir(os.path.join(country_input_folder, f))])

    #iterate over each subfolder and each subdivision flag, creating a custom and unique CSS class selector for each   
    for country in all_folders:
        all_files = [f for f in os.listdir(os.path.join(country_input_folder, country)) if os.path.isfile(os.path.join(country_input_folder, country, f))]
        all_files.sort()
        for file in all_files:
            #ignore readme and ds_store file
            if (os.path.splitext(file)[0].lower() == "readme" or file.lower() == ".ds_store"):
                continue
            # css_output_str += "\n.fi-" + country.lower() + "-" + os.path.splitext(file)[0].lower() + " {\n" + "\tbackground-image: url(" + country_input_folder + "/" + country + "/" + file + ");\n}\n"
            css_output_str += "\n.fi-" + os.path.splitext(file)[0].lower() + " {\n" + "\tbackground-image: url(" + country_input_folder + "/" + country + "/" + file + ");\n}\n"

    #append output string to CSS file
    with open(export_css_filepath, "a") as css_file:
        css_file.write(css_output_str)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for generating the iso3166-1.css and iso3166-2.css files.')

    parser.add_argument('-iso3166_1_country_input_folder', '--iso3166_1_country_input_folder', type=str, required=False, default="iso3166-1-flags", 
        help='Input folder of ISO 3166-1 flags.')
    parser.add_argument('-iso3166_2_country_input_folder', '--iso3166_2_country_input_folder', type=str, required=False, default="iso3166-2-flags", 
        help='Input folder of ISO 3166-2 flags.')
    parser.add_argument('-export_iso3166_1_css_filepath', '--export_iso3166_1_css_filepath', type=str, required=False, default="iso3166-1-flags-test.css", 
        help='Export filepath for generated ISO 3166-1 CSS file.')
    parser.add_argument('-export_iso3166_2_css_filepath', '--export_iso3166_2_css_filepath', type=str, required=False, default="iso3166-2-flags-test.css", 
        help='Export filepath for generated ISO 3166-2 CSS file.')
    parser.add_argument('-iso3166_type', '--iso3166_type', type=str, required=False, default="", 
        help='Create ISO 3166-1 or ISO 3166-2 CSS file. If empty, both will be generated.')

    #parse input args
    args = parser.parse_args()
    iso3166_1_country_input_folder = args.iso3166_1_country_input_folder
    iso3166_2_country_input_folder = args.iso3166_2_country_input_folder
    export_iso3166_1_css_filepath = args.export_iso3166_1_css_filepath
    export_iso3166_2_css_filepath = args.export_iso3166_2_css_filepath
    iso3166_type = args.iso3166_type

    #create CSS file for either ISO 3166-1 or ISO 3166-2, or both
    if (iso3166_type.lower() == "iso3166-1"):
        create_iso3166_1_css(country_input_folder=iso3166_1_country_input_folder, export_css_filepath=export_iso3166_1_css_filepath)
    elif (iso3166_type.lower() == "iso3166-2"):
        create_iso3166_2_css(country_input_folder=iso3166_2_country_input_folder, export_css_filepath=export_iso3166_2_css_filepath)
    else:
        create_iso3166_1_css(country_input_folder=iso3166_1_country_input_folder, export_css_filepath=export_iso3166_1_css_filepath)
        create_iso3166_2_css(country_input_folder=iso3166_2_country_input_folder, export_css_filepath=export_iso3166_2_css_filepath)