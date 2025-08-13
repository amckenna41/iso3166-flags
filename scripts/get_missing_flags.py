from iso3166_2 import Subdivisions
import pandas as pd
import argparse
import os

def export_missing_flags(flag_icons_dir: str, export: bool=True, export_filename: str="missing_subdivision_flags.csv") -> None:
    """
    Export a list of subdivisions that do not have a supported flag in the inputted folder, 
    using the custom-built iso3166-2 software package. Many subdivisions do not have an 
    officially recognized or associated flag. The list will be exported to a DataFrame & 
    CSV, listing the subdivision code & name. The output will be sorted alphabetically.

    Parameters
    ==========
    :flag_icons_dir: str
        path to folder of flag icons.
    :export: bool (default=True)
        whether to export the list of missing subdivision flags to CSV.
    :export_filename: str (default="missing_subdivisions_flags.csv")
        name of export file.

    Returns
    =======
    :missing_files_df: pd.DataFrame
        dataframe of missing flags list including subdivision code & name.

    Raises
    ======
    OSError
        Flag folder not found.
    """
    #create instance of the super duper amazingly custom-built iso3166-2 class
    subdivisions = Subdivisions()

    #get object of subdivision codes
    all_subdivision_codes = subdivisions.subdivision_codes()

    #intialise dataframe that will store rows of missing subdivisions, their codes and names
    missing_files_df = pd.DataFrame(columns=["subdivisionCode", "subdivisionName"])

    #object of all files, the parent folder is the key
    all_files = {}

    #raise error if folder of images not found
    if not (os.path.isdir(flag_icons_dir)):
        raise OSError(f"Folder of flag images not found: {flag_icons_dir}.")

    #iterate through the flag folder & sub-folders (if applicable)
    for folder_path, _, filenames in os.walk(flag_icons_dir):

        #get parent folder 
        parent_folder = os.path.basename(folder_path)
            
        #initialize an entry in the dictionary for the parent folder if not already present
        if (parent_folder not in all_files):
            all_files[parent_folder] = []

        #iterate over the filenames in the current folder
        for filename in filenames:
            #skip markdown files
            if (filename == "README.md"):
                continue
            #add the filename, without its extension, to the dictionary under the parent folder key
            all_files[parent_folder].append(os.path.splitext(filename)[0])

    #list to store new rows
    new_rows = []

    #iterate through all subdivisions, append any subdivisions that don't have an associated flag to the dataframe
    for country in all_subdivision_codes:
        for subd in all_subdivision_codes[country]:
            if (country not in all_files or subd not in all_files[country]):
                subdivision_name = subdivisions[country][subd]["name"]
                #wrap in double quotes subdivision names with commas in them 
                if ("," in subdivision_name):
                    subdivision_name = f'"{subdivision_name}"'  # Wrap in double quotes

                #add subdivision data to object
                new_row = {"subdivisionCode": subd, "subdivisionName": subdivision_name}
                new_rows.append(new_row)
    
    #append csv extension to file if no extension or invalid extension
    if (os.path.splitext(export_filename)[1] != ".csv"):
        export_filename = export_filename + ".csv"

    #concatenate list of missing subdivision rows to main dataframe 
    missing_files_df = pd.concat([missing_files_df, pd.DataFrame(new_rows)], ignore_index=True)

    #export dataframe to csv
    if (export):
        missing_files_df.to_csv(export_filename, index=False)

    return missing_files_df

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting file of any subdivisions that do not have an associated flag in the repo.')

    parser.add_argument('-flag_icons_dir', '--flag_icons_dir', type=str, required=False, default="iso3166-2-icons-edit-this-one", help='Input folder of ISO 3166-2 flag icons.')
    parser.add_argument('-export_filename', '--export_filename', type=str, required=False, default="missing-iso3166-2-icons", help='Export filename for missing subdivisions/flags csv.')

    #parse input args
    args = parser.parse_args()
    flag_icons_dir = args.flag_icons_dir
    export_filename = args.export_filename

    #call missing subdivisions function
    export_missing_flags(vars(**args))