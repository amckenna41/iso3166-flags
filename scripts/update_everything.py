import os
import time
from generate_css import *
from generate_readme import *
from get_flag_metadata import *
from get_missing_flags import *

def update_everything(output_folder: str="") -> None:
    """
    Script that ensures all the data files and metadata objects used throughout 
    the iso3166-flag-icons project are kept up-to-date when any flags have been 
    added, changed or deleted. If any updates are made to the flag directories, 
    several files throughout the repo may become out of date as their data source 
    is the dataset of flags.

    This script should be executed anytime a flag change is made to the dataset. 
    Once executed the script will update the two CSS files, the individual markdown 
    files in each country subfolder in /iso3166-2-icons, the 2 flag directory 
    metadata files and updates the list of missing subdivision flags. 

    Parameters
    ==========
    :output_folder: str (default="")
        folder to store all the outputs and metadata.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Flag or CSS directories not found. 
    """
    #iso3166-1/2 folder names
    iso3166_1_dir = "iso3166-1-icons"
    iso3166_2_dir = "iso3166-2-icons"

    #path to CSS directory
    css_dir = "css"

    #raise OSError if the flag or CSS directories aren't found
    if not (os.path.isdir(iso3166_1_dir) or not (os.path.isdir(iso3166_2_dir)) or not (os.path.isdir(css_dir))):
        raise OSError("Flag or CSS directories not found, double check they are on the path.")

    #start timer
    start = time.time()

    #create the iso3166-1 and iso3166-2 CSS files
    create_iso3166_1_css(country_input_folder=iso3166_1_dir, export_css_filepath=os.path.join(css_dir, "iso3166-1.css"))
    create_iso3166_2_css(country_input_folder=iso3166_1_dir, export_css_filepath=os.path.join(css_dir, "iso3166-2.css"))

    #create markdown file for each country subfolder for subdivision flags
    create_readme(iso3166_2_dir)

    #export individual flag metadata for the ISO 3166-1 and ISO 3166-2 flags 
    export_flag_metadata("iso3166-1-icons", flag_metadata_output="iso3166_1_flag_metadata.csv")
    export_flag_metadata("iso3166-2-icons", flag_metadata_output="iso3166_2_flag_metadata.csv")

    #export metadata on full repo
    export_repo_metadata(export_json=True, export_filename="repo_metadata", exclude_readme=True)

    #export list of missing subdivision flags
    export_missing_flags("iso3166-2-icons", export=True, export_filename="missing_subdivision_flags.csv")

    #stop counter and calculate elapsed time
    end = time.time()
    elapsed = end - start

    print('\n######################################################################\n')
    print("Update complete...")
    print(f"\nElapsed Time for exporting and updating all iso3166-flag-icons data and metadata files: {(elapsed / 60):.2f} minutes.")

if __name__ == '__main__':
    update_everything()