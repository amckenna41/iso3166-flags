import os
import sys
import time
import argparse
import shutil
import tempfile
import filecmp

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

def update_everything(dry_run: bool=False, check: bool=False) -> list:
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
    :dry_run: bool (default=False)
        If True, preview changes without modifying actual files. Files are written
        to a temporary directory and differences are shown. Use this to verify
        changes before running the full update.
    :check: bool (default=False)
        If True, run in dry-run mode and compare the freshly generated CSS/README/metadata
        files against the versions currently committed in the repo, without modifying
        anything. Intended for use as a CI staleness gate that fails when flags have been
        added/changed without the derived files being regenerated via this script.

    Returns
    =======
    :stale_files: list
        list of committed file paths that differ from their freshly generated counterpart.
        Always empty unless check=True.

    Raises
    ======
    OSError:
        Flag or CSS directories not found.
    """
    #a staleness check implies generating into a temp dir like a dry-run, without touching real files
    dry_run = dry_run or check

    #iso3166-1/2 folder names
    iso3166_1_dir = "iso3166-1-flags"
    iso3166_2_dir = "iso3166-2-flags"
    iso3166_metadata_dir = "iso3166-flags-metadata"

    #path to CSS directory
    css_dir = "css"

    #raise OSError if the flag or CSS directories aren't found
    if not (os.path.isdir(iso3166_1_dir) and os.path.isdir(iso3166_2_dir) and os.path.isdir(css_dir)):
        raise OSError("Flag or CSS directories not found, double check they are on the path.")

    #list of committed files found to be out of sync with their freshly generated counterpart, only populated if check=True
    stale_files = []

    # Setup output directories based on dry-run mode
    if dry_run:
        temp_dir = tempfile.mkdtemp(prefix="iso3166_dry_run_")
        temp_css_dir = os.path.join(temp_dir, "css")
        temp_metadata_dir = os.path.join(temp_dir, "metadata")
        temp_readme_dir = os.path.join(temp_dir, "iso3166-2-flags-readme")

        os.makedirs(temp_css_dir, exist_ok=True)
        os.makedirs(temp_metadata_dir, exist_ok=True)
        os.makedirs(temp_readme_dir, exist_ok=True)

        actual_css_dir = css_dir
        actual_metadata_dir = iso3166_metadata_dir

        css_dir = temp_css_dir
        iso3166_metadata_dir = temp_metadata_dir

        print("\n" + "="*70)
        print("DRY RUN MODE - No files will be modified")
        print(f"Temporary directory: {temp_dir}")
        print("="*70)
    else:
        temp_dir = None
        temp_readme_dir = None

    #start timer
    start = time.time()

    try:
        if not dry_run:
            #convert any gif or webp files to PNG
            convert_img(flag_folder=iso3166_2_dir, img_format="png", delete_original=1)

        #create the iso3166-1 and iso3166-2 CSS files (and their minified counterparts)
        create_iso3166_1_css(country_input_folder=iso3166_1_dir, export_css_filepath=os.path.join(css_dir, "iso3166-1.css"), minify=True)
        create_iso3166_2_css(country_input_folder=iso3166_2_dir, export_css_filepath=os.path.join(css_dir, "iso3166-2.css"), minify=True)

        #create markdown file for each country subfolder for subdivision flags - in dry-run mode, write each
        #country's README into the temp directory instead of its real subfolder so no files are touched
        if dry_run:
            for country_code in sorted(os.listdir(iso3166_2_dir)):
                if os.path.isdir(os.path.join(iso3166_2_dir, country_code)):
                    create_readme(iso3166_2_dir, country_subfolder=country_code, output_readme_folder=temp_readme_dir)
        else:
            create_readme(iso3166_2_dir)

        #export individual flag metadata for the ISO 3166-1 and ISO 3166-2 flags 
        export_flag_metadata("iso3166-1-flags", flag_metadata_output=os.path.join(iso3166_metadata_dir, "iso3166_1_flag_metadata.csv"))
        export_flag_metadata("iso3166-2-flags", flag_metadata_output=os.path.join(iso3166_metadata_dir, "iso3166_2_flag_metadata.csv"))

        #export metadata on full repo
        export_repo_metadata(export_json=True, export_filename=os.path.join(iso3166_metadata_dir, "iso3166_flags_metadata.json"), exclude_readme=True)

        #export list of missing subdivision flags - redirect to the temp dir in dry-run mode so the real file isn't touched
        missing_flags_export_filename = os.path.join(temp_dir, "missing_subdivision_flags.csv") if dry_run else "missing_subdivision_flags.csv"
        export_missing_flags("iso3166-2-flags", export=True, export_filename=missing_flags_export_filename)

        #compare the freshly generated files against what's currently committed, flagging any that are out of sync
        if check:
            generated_pairs = [
                (os.path.join(actual_css_dir, "iso3166-1.css"), os.path.join(css_dir, "iso3166-1.css")),
                (os.path.join(actual_css_dir, "iso3166-1.min.css"), os.path.join(css_dir, "iso3166-1.min.css")),
                (os.path.join(actual_css_dir, "iso3166-2.css"), os.path.join(css_dir, "iso3166-2.css")),
                (os.path.join(actual_css_dir, "iso3166-2.min.css"), os.path.join(css_dir, "iso3166-2.min.css")),
                (os.path.join(actual_metadata_dir, "iso3166_1_flag_metadata.csv"), os.path.join(iso3166_metadata_dir, "iso3166_1_flag_metadata.csv")),
                (os.path.join(actual_metadata_dir, "iso3166_2_flag_metadata.csv"), os.path.join(iso3166_metadata_dir, "iso3166_2_flag_metadata.csv")),
                (os.path.join(actual_metadata_dir, "iso3166_flags_metadata.json"), os.path.join(iso3166_metadata_dir, "iso3166_flags_metadata.json")),
            ]
            for country_code in sorted(os.listdir(iso3166_2_dir)):
                if os.path.isdir(os.path.join(iso3166_2_dir, country_code)):
                    generated_pairs.append((
                        os.path.join(iso3166_2_dir, country_code, "README.md"),
                        os.path.join(temp_readme_dir, country_code, "README.md"),
                    ))

            for committed_path, generated_path in generated_pairs:
                #a committed file missing its generated counterpart, or differing in content, counts as stale
                if not os.path.isfile(generated_path) or not os.path.isfile(committed_path) or not filecmp.cmp(committed_path, generated_path, shallow=False):
                    stale_files.append(committed_path)

        #stop counter and calculate elapsed time
        end = time.time()
        elapsed = end - start

        print('\n######################################################################\n')
        if check:
            if stale_files:
                print(f"STALE: {len(stale_files)} committed file(s) are out of sync with the flag directories:")
                for stale_file in stale_files:
                    print(f"  - {stale_file}")
            else:
                print("All generated CSS/README/metadata files are up to date.")
        elif dry_run:
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
            print(f"  - Markdown files in {iso3166_2_dir}/*/ subdirectories")
            
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

    return stale_files

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
        '--check',
        action='store_true',
        help='Check whether the committed CSS/README/metadata files are stale relative to the flag directories, '
             'without modifying anything. Exits non-zero if anything is stale (for use as a CI gate).'
    )

    args = parser.parse_args()
    stale_files = update_everything(dry_run=args.dry_run, check=args.check)

    if args.check and stale_files:
        sys.exit(1)