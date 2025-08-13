import os
import argparse
import iso3166
from iso3166_2 import *

#base URL to iso3166-2-icons folder in repo
base_url = 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons'

def create_markdown_str(country_code: str, input_folder: str) -> None:
    """
    Create custom README for inputted country's subdivision folder. This function compiles
    the output string which is appended to the country folder's README. The README will list 
    various useful data about the country/territory along with listing all of its ISO 3166-2 
    subdivisions, including their name, code, type, flag preview, link to flag & link to the 
    country's data on the iso3166-2 API. It will also list those subdivisions that have no
    associated flag. The function can accept the ISO 3166-1 country code in its alpha-2, alpha-3 
    or numeric country code, which will then be converted into alpha-2.

    Parameters
    ==========
    :country_code: string 
        ISO 3166-1 code of country.
    :input_folder: string
        filepath to input folder to write README.
        
    Returns
    =======
    :output_str: str
        string of subdivision data per country which is appended to the README file. 
    
    Raises
    ======
    ValueError:
        More than 1 country code input to function.
    OSError:
        Folder of flags not found.
    """  
    #convert the input country code into its alpha-2 form
    country_code = convert_to_alpha2(country_code)
    
    #get list of all files in country's subfolder, remove readme and DS_Store file from list of files, if applicable
    if not (os.path.isdir(os.path.join(input_folder, country_code))):
        if (os.path.isdir(os.path.join(input_folder))):
            all_files = sorted(
                [f for f in os.listdir(os.path.join(input_folder)) if os.path.isfile(os.path.join(input_folder, f)) and f not in {"README.md", ".DS_Store"}],
                key=str.casefold
            )
        else:
            #raise error if input folder not found 
            raise OSError(f"Input folder of flags/sub-folders not found {input_folder}.")
    else:
            #if country code sub-folder does exist, list from that sub-folder instead
            all_files = sorted(
                [f for f in os.listdir(os.path.join(input_folder, country_code)) if os.path.isfile(os.path.join(input_folder, country_code, f)) and f not in {"README.md", ".DS_Store"}],
                key=str.casefold
            )     

    #create instance of Subdivision class from amazingly perfect beautiful and wonderful iso3166-2 package
    subdivisions = Subdivisions()

    #get list of country's subdivisions
    all_subdivisions = subdivisions[country_code] 

    #get country name from iso3166 library
    country_name = iso3166.countries_by_alpha2[country_code].name

    #append subdivision name, code and flag emoji to top of readme
    output_str = ""
    output_str = f"# {country_name} Subdivisions ![](https://flagcdn.com/h40/{country_code.lower()}.png)\n\n"
    output_str += f"- **ISO Code**: {country_code}\n"

    #get list of all subdivision types for country
    subdivision_types = sorted({entry["type"] for entry in all_subdivisions.values() if "type" in entry})

    #add some useful data about the country's subdivision 
    output_str += f"- **Number of subdivisions**: {len(all_subdivisions)}\n"
    output_str += f"- **Subdivision Type**: {', '.join(subdivision_types)}\n"
    output_str += f"- **ISO 3166-2 API link**: https://iso3166-2-api.vercel.app/api/alpha/{country_code}\n\n"

    #create table that will display each subdivisions code, name, type, flag & link on repo
    output_str += "| Code  | Subdivision Name         | Type | Flag Preview | Link |\n"
    output_str += "|-------|--------------------------|--------------| -------------- |----------|\n"

    #iterate through all file names/subdivisions, appending to the output string 
    for file in all_files:

        #parse subdivision code from filename
        subd_code = os.path.splitext(file)[0]

        #raise error if subdivision code not found in list for current country
        if not (subd_code in all_subdivisions):
            raise ValueError(f"Subdivision code {subd_code} not found in list of available subdivision codes for {country_code}.")
        
        #parse subdivision code from object, append to string
        current_subdivision = all_subdivisions[subd_code]

        #add subdivision and its data to table row
        output_str += f"| {subd_code} | {current_subdivision.name} | {current_subdivision.type} | <img src='{current_subdivision['flag']}' height='80'> | [{subd_code}]({base_url}/{country_code}/{file}) |\n"

    #get list of file names, remove extension    
    all_files_no_extension = [os.path.splitext(file)[0] for file in all_files]
    
    #list of subdivisions that dont have flags in the respective folder
    missing_subdivisions = []

    #get list of missing subdivision flags not present in country subfolder
    for subd in all_subdivisions:
        if (subd not in all_files_no_extension):
            missing_subdivisions.append(subd)
    
    #print list of country's subdivisions that don't have any associated flags
    if len(missing_subdivisions) != 0:
        output_str += f'\n{country_name} ISO 3166-2 subdivisions with no available flags:\n'
        for subd in sorted(missing_subdivisions):
            for subdiv in all_subdivisions:
                if (subdiv == subd):
                    output_str += f"\n* **{subd.upper()}: {all_subdivisions[subdiv].name} ({all_subdivisions[subdiv].type})**"

    return output_str

def create_readme(flag_input_folder: str, country_subfolder: str="", output_readme_folder: str="") -> None:
    """ 
    Create custom README for all country sub-folders in the inputted flag folder. The 
    README will list various useful data about the country/territory along with listing all 
    of its ISO 3166-2 subdivisions, including their name, code, type, flag preview, link to 
    flag & link to the country's data on the iso3166-2 API. It will also append all those 
    subdivisions that do not have a corresponding flag on the repo.

    The function typically accepts a folder of country sub-folders but you can also pass
    in a specific country subfolder via the country_subfolder parameter which will take
    precedence over the flag_input_folder parameter. The function will only generate
    the readme within a subfolder of flags and won't generate it for individual flags
    in a folder.
    
    Parameters
    ==========
    :flag_input_folder: str
        input path to folder/sub-folders of flags to generate readme for.
    :country_subfolder: str (default="")
        individual country subfolder to generate readme for.
    :output_readme_folder: str (default="")
        folder to store the generated markdown files. By default these will be stored
        in the country's respective subfolder. 

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Flag folder/sub-folder not found.
        Invalid filepath to README.md file.
    ValueError:
        Invalid country code subfolder.
    """
    #raise error if folder of images not found
    if not (os.path.isdir(flag_input_folder)):
        raise OSError(f"Folder of flag images not found: {flag_input_folder}.")

    #if no individual country subfolder/country code input then get list of all sub-folders
    if (country_subfolder == ""):
        #get list of ISO 3166-2 country sub-folders
        iso3166_2_folder = sorted([i for i in os.listdir(flag_input_folder) if os.path.isdir(os.path.join(flag_input_folder, i))])

        #set folder name to the basename if it is already a country code subfolder
        if not (iso3166_2_folder):
            files = [i for i in os.listdir(flag_input_folder) if os.path.isfile(os.path.join(flag_input_folder, i))]
            if (files):
                iso3166_2_folder = [os.path.basename(flag_input_folder)]

        #iterate over all ISO 3166-2 sub-folders and create custom readme file
        for country_code in iso3166_2_folder:
                
            #raise error if invalid subfolder/iso 3166 country code
            if not (country_code in list(iso3166.countries_by_alpha2)):
                raise ValueError(f"Country code subfolder invalid and not in the ISO 3166 list of code: {country_code}.")

            #get readme file contents for current subfolder
            readme_string = create_markdown_str(country_code, flag_input_folder)

            #get filepath to readme file in each input folder
            filepath = "{}/{}".format(flag_input_folder, country_code)

            #raise error if invalid filepath to readme
            if not (os.path.isdir(os.path.join(flag_input_folder, country_code))):
                if (os.path.isdir(os.path.join(flag_input_folder))):
                    filepath = flag_input_folder
                else:
                    raise OSError(f"Invalid filepath to README {flag_input_folder}.")
            else:
                filepath = f"{flag_input_folder}/{country_code}"

            read_me_filepath = os.path.join(filepath, 'README.md')
            
            #append output string to readme
            with open(read_me_filepath, "w") as readme_file:
                readme_file.write(readme_string)
    else:
        #convert country code into ISO 3166-1 alpha-2 format
        country_code = convert_to_alpha2(country_subfolder)

        #get coountry subfolder path
        country_subfolder = os.path.join(flag_input_folder, country_subfolder)

        #raise error if subfolder an invalid path
        if not (os.path.isdir(country_subfolder)):
            raise OSError(f"Invalid path to inputted country subfolder: {country_subfolder}.")

        #get readme file contents for inputted subfolder
        readme_string = create_markdown_str(country_code, flag_input_folder)

        #get filepath to readme file in each input folder OR set filepath to the custom markdown export folder
        if (output_readme_folder != ""):
            filepath = os.path.join(output_readme_folder, country_code)
        else:
            filepath = os.path.join(flag_input_folder, country_code)

        #create directory to store readme file if not present
        if not (os.path.isdir(filepath)):
            os.makedirs(filepath)

        #get full filepath for output markdown    
        read_me_filepath = os.path.join(filepath, 'README.md')

        #append output string to readme & export
        with open(read_me_filepath, "w") as readme_file:
            readme_file.write(readme_string)

def convert_to_alpha2(alpha_code: str) -> str:
    """ 
    Auxiliary function that converts an ISO 3166 country's 3 letter alpha-3 
    or numeric country code into its 2 letter alpha-2 counterpart. The 
    function also validates the input alpha-2 or converted alpha-2 code, 
    raising an error if it is invalid. 

    Parameters 
    ==========
    :alpha_code: str
        3 letter ISO 3166-1 alpha-3 or numeric country code.
    
    Returns
    =======
    :iso3166.countries_by_alpha3[alpha_code].alpha2|iso3166.countries_by_numeric[alpha_code].alpha: str
        2 letter ISO 3166 alpha-2 country code. 
    
    Raises
    ======
    TypeError:
        Invalid data type for alpha code parameter input.
    ValueError:
        Issue converting the inputted alpha code into alpha-2 code.
    """
    #raise error if invalid type input
    if not (isinstance(alpha_code, str)):
        raise TypeError(f"Expected input alpha code to be a string, got {type(alpha_code)}.")

    #raise error if more than 1 country code input
    if ("," in alpha_code):
        raise ValueError(f"Only one country code should be input into the function: {alpha_code}.")
    
    #uppercase alpha code, initial_alpha_code var maintains the original alpha code pre-uppercasing
    alpha_code = alpha_code.upper().replace(' ', '')
    initial_alpha_code = alpha_code
    
    #use iso3166 package to find corresponding alpha-2 code from its numeric code, return error if numeric code not found
    if (alpha_code.isdigit()):
        if not (alpha_code in list(iso3166.countries_by_numeric.keys())):
            raise ValueError(f"Invalid ISO 3166-1 alpha numeric country code input: {initial_alpha_code}.")
        return iso3166.countries_by_numeric[alpha_code].alpha2

    #return input alpha code if its valid, return error if alpha-2 code not found
    if len(alpha_code) == 2:
        if not (alpha_code in list(iso3166.countries_by_alpha2.keys())):
            raise ValueError(f"Invalid ISO 3166-1 alpha-2 country code input: {initial_alpha_code}.")
        return alpha_code

    #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code, return error if code not found
    if len(alpha_code) == 3:
        if not (alpha_code in list(iso3166.countries_by_alpha3.keys())):
            raise ValueError(f"Invalid ISO 3166-1 alpha-3 country code: {initial_alpha_code}.")
        return iso3166.countries_by_alpha3[alpha_code].alpha2

    #return error by default if input code not returned already
    raise ValueError(f"Invalid ISO 3166-1 alpha country code input: {alpha_code}.")
    
if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for generating the markdown files for each countrys subdivision folders.')

    parser.add_argument('-flag_input_folder', '--flag_input_folder', type=str, required=False, default="iso3166-2-icons-edit-this-one", 
        help='Input folder of ISO 3166-2 flag icons to generate README for.')
    parser.add_argument('-country_subfolder', '--country_subfolder', type=str, required=False, default="", 
        help='Specific subfolder of country subdivisions to generate README for. If a subfolder and main folder name are input this arg will take precedence.')
    parser.add_argument('-output_readme_folder', '--output_readme_folder', type=str, required=False, default="", 
        help='Specific output folder to store the generated markdown files, by default they will be stored within the countrys subfolder.')
    
    #parse input args
    args = parser.parse_args()
    
    #create readme for input folder of flags or individual subfolder
    create_readme(**vars(args))