import os
import time
import argparse
import shutil
import tempfile

# Support both direct script execution and module execution
try:
    # Relative imports (for python3 -m scripts.update_everything)
    from .generate_css import *
    from .generate_readme import *
    from .get_flag_metadata import *
    from .get_missing_flags import *
    from .convert_images import *
except ImportError:
    # Absolute imports (for python3 scripts/update_everything.py or running from scripts dir)
    from generate_css import *
    from generate_readme import *
    from get_flag_metadata import *
    from get_missing_flags import *
    from convert_images import *

def update_everything(output_folder: str="", dry_run: bool=False) -> None:
    """
    Script that ensures all the data files and metadata objects used throughout 
    the iso3166-flags project are kept up-to-date when any flags have been 
    added, changed or deleted. If any updates are made to the flag directories, 
    several files throughout the repo may become out of date as their data source 
    is the dataset of flags.

    This script should be executed anytime a flag change is made to the dataset. 
    Once executed the script will update the two CSS files, the individual markdown 
    files in each country subfolder in /iso3166-2-flags, the 2 flag directory 
    metadata files and updates the list of missing subdivision flags. 

    Parameters
    ==========
    :output_folder: str (default="")
        folder to store all the outputs and metadata.
    :dry_run: bool (default=False)
        If True, preview changes without modifying actual files. Files are written
        to a temporary directory and differences are shown. Use this to verify
        changes before running the full update.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Flag or CSS directories not found. 
    """
    #iso3166-1/2 folder names
    iso3166_1_dir = "iso3166-1-flags"
    iso3166_2_dir = "iso3166-2-flags"
    iso3166_metadata_dir = "iso3166-flags-metadata"

    #path to CSS directory
    css_dir = "css"

    #raise OSError if the flag or CSS directories aren't found
    if not (os.path.isdir(iso3166_1_dir) and os.path.isdir(iso3166_2_dir) and os.path.isdir(css_dir)):
        raise OSError("Flag or CSS directories not found, double check they are on the path.")

    # Setup output directories based on dry-run mode
    if dry_run:
        temp_dir = tempfile.mkdtemp(prefix="iso3166_dry_run_")
        temp_css_dir = os.path.join(temp_dir, "css")
        temp_metadata_dir = os.path.join(temp_dir, "metadata")
        temp_iso3166_2_dir = os.path.join(temp_dir, "iso3166-2-flags")
        
        os.makedirs(temp_css_dir, exist_ok=True)
        os.makedirs(temp_metadata_dir, exist_ok=True)
        os.makedirs(temp_iso3166_2_dir, exist_ok=True)
        
        actual_css_dir = css_dir
        actual_metadata_dir = iso3166_metadata_dir
        actual_iso3166_2_dir = iso3166_2_dir
        
        css_dir = temp_css_dir
        iso3166_metadata_dir = temp_metadata_dir
        iso3166_2_dir = temp_iso3166_2_dir
        
        print("\n" + "="*70)
        print("DRY RUN MODE - No files will be modified")
        print(f"Temporary directory: {temp_dir}")
        print("="*70)
    else:
        temp_dir = None

    #start timer
    start = time.time()

    try:
        if not dry_run:
            #convert any gif or webp files to PNG
            convert_img(flag_folder=iso3166_2_dir, img_format="png", delete_original=1)

        #create the iso3166-1 and iso3166-2 CSS files (and their minified counterparts)
        create_iso3166_1_css(country_input_folder=iso3166_1_dir, export_css_filepath=os.path.join(css_dir, "iso3166-1.css"), minify=True)
        create_iso3166_2_css(country_input_folder=iso3166_2_dir, export_css_filepath=os.path.join(css_dir, "iso3166-2.css"), minify=True)

        #create markdown file for each country subfolder for subdivision flags
        create_readme(iso3166_2_dir)

        #export individual flag metadata for the ISO 3166-1 and ISO 3166-2 flags 
        export_flag_metadata("iso3166-1-flags", flag_metadata_output=os.path.join(iso3166_metadata_dir, "iso3166_1_flag_metadata.csv"))
        export_flag_metadata("iso3166-2-flags", flag_metadata_output=os.path.join(iso3166_metadata_dir, "iso3166_2_flag_metadata.csv"))

        #export metadata on full repo
        export_repo_metadata(export_json=True, export_filename=os.path.join(iso3166_metadata_dir, "iso3166_flags_metadata.json"), exclude_readme=True)

        #export list of missing subdivision flags
        export_missing_flags("iso3166-2-flags", export=True, export_filename="missing_subdivision_flags.csv")

        #stop counter and calculate elapsed time
        end = time.time()
        elapsed = end - start

        print('\n######################################################################\n')
        if dry_run:
            print("DRY RUN: Preview complete (no changes made)")
            print(f"\nFiles that would be updated:")
            print(f"  - {os.path.join(actual_css_dir, 'iso3166-1.css')}")
            print(f"  - {os.path.join(actual_css_dir, 'iso3166-1.min.css')}")
            print(f"  - {os.path.join(actual_css_dir, 'iso3166-2.css')}")
            print(f"  - {os.path.join(actual_css_dir, 'iso3166-2.min.css')}")
            print(f"  - {os.path.join(actual_metadata_dir, 'iso3166_1_flag_metadata.csv')}")
            print(f"  - {os.path.join(actual_metadata_dir, 'iso3166_2_flag_metadata.csv')}")
            print(f"  - {os.path.join(actual_metadata_dir, 'iso3166_flags_metadata.json')}")
            print(f"  - missing_subdivision_flags.csv")
            print(f"  - Markdown files in {actual_iso3166_2_dir}/*/ subdirectories")
            
            # Show sample of what was generated
            css_file = os.path.join(css_dir, "iso3166-1.css")
            if os.path.isfile(css_file):
                with open(css_file, 'r') as f:
                    lines = f.readlines()[:5]
                print(f"\nSample CSS output (first 5 lines of iso3166-1.css):")
                print("".join(lines))
        else:
            print("Update complete...")
            print(f"\nElapsed Time for exporting and updating all iso3166-flags data and metadata files: {(elapsed / 60):.2f} minutes.")
        
        print(f"\nExecution time: {(elapsed / 60):.2f} minutes.")
        
    finally:
        # Clean up temporary directory if in dry-run mode
        if dry_run and temp_dir and os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
            print("\nTemporary files cleaned up.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Update all iso3166-flags project metadata, CSS, and documentation files."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files. Files are written to a temporary directory and cleaned up after.'
    )
    parser.add_argument(
        '-o', '--output',
        default='',
        help='Output folder for storing metadata and other generated files (optional).'
    )
    
    args = parser.parse_args()
    update_everything(output_folder=args.output, dry_run=args.dry_run)