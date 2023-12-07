"""
Create JSON files for both ISO3166-1 and ISO3166-2 flag icons allowing for easy integration
of country and subdivision flags into a front-end project. 
The ISO3166-1 json holds the country name, country ISO code and filepath to flag in 
iso3166-1-icons folder. 
Two JSON files are created for the ISO3166-2 flags, the first - iso3166-2-min.json - is a condensed
file that just includes the country name, ISO code, subdivision names and filepaths to each 
respective subdivision in the iso3166-2-icons folder. The second file - iso3166-2.json - 
contains the aforementioned info as well as additional country info using the rest countries
api (https://restcountries.com/). 
"""
import os
import json
import argparse
import requests
import logging
import getpass
from urllib.parse import unquote
import pycountry
import iso3166_
import re

#initialise logging library 
__version__ = "1.0.1"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-flag-icons/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-flag-icons', getpass.getuser())}


def createISO3166_1_Json(countryInputFolder="../iso3166-1-icons"):
    """
    Create JSON file for all ISO3166-1 flag icons, JSON will include the countrys full name,
    2 letter ISO code and full path to its URL in repo. JSON used for importing and displaying
    flags in index.html front-end demo.

    Parameters
    ----------
    : countryInputFolder : str (default="../iso3166-1-icons")
        filepath to folder containing all ISO3166-1 icons.

    Returns
    -------
    None
    """
    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join("../", "iso3166-1.json")

    #object for storing all json output data
    json_data = []

    #get sorted list of all ISO3166-1 svg files 
    allFiles = sorted([f for f in os.listdir(countryInputFolder) if os.path.isfile(os.path.join(countryInputFolder, f))])

    #iterate over all svg files in folder, appending country name, code and filepath/url to json
    for country in allFiles:
        #ignore readme file
        if (country.lower() == "readme.md"):
            continue
        
        #get country name using the 2 letter ISO code
        countryCode = os.path.splitext(country)[0].upper()
        if (pycountry.countries.get(alpha_2=countryCode) == None):
            countryName = iso3166_.countries_by_alpha2[countryCode.upper()].name
        else:
            countryName = pycountry.countries.get(alpha_2=countryCode).name

        #append to json
        json_data.append({"Country": countryName, "Code": countryCode, "Flag": os.path.join(countryInputFolder, country)})

    #write json data to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        

def createISO3166_2_Json(countryInputFolder="../iso3166-2-icons"):
    """
    Create JSON file for all ISO3166-2 flag icons. The min JSON file will include the countrys full name,
    2 letter ISO code, list of subdivision code and path to each respective flag. The other JSON
    will include the last 4 mentioned parameters as well as each country's info from the restcountries
    api. The JSON's will be used for importing and displaying flags in index.html front-end demo.

    Parameters
    ----------
    : countryInputFolder : str (default="../iso3166-2-icons")
        filepath to folder containing all ISO3166-2 subdivisions.

    Returns
    -------
    None
    """
    #arrays for store all json parameters
    json_data = []
    json_min_data = []

    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join("../", "iso3166-2.json")
    json_min_filepath = os.path.join("../", os.path.splitext("iso3166-2.json")[0] + '-min' + os.path.splitext("iso3166-2.json")[1])
    
    json_filepath = os.path.join("../", "test-iso3166-2.json")
    json_min_filepath = os.path.join("../", os.path.splitext("test-iso3166-2.json")[0] + '-min' + os.path.splitext("iso3166-2.json")[1])
    
    #get sorted list of all ISO3166-2 subfolders
    allFolders = sorted([f for f in os.listdir(countryInputFolder) if os.path.isdir(os.path.join(countryInputFolder, f))])
    countryIndex = 0

    print(allFolders)
    #iterate over all subdivision folders, getting country and subdivision info, append to json's
    for folder in allFolders:

        #get sorted list of files in country's folder
        allFiles = sorted([f for f in os.listdir(os.path.join(countryInputFolder, folder)) if os.path.isfile(os.path.join(countryInputFolder, folder, f))])
        
        country_url = "https://restcountries.com/v3.1/alpha/" + folder

        #get country info from restcountries api
        restCountriesResponse = requests.get(country_url, stream=True, headers=USER_AGENT_HEADER)
        #raise error if invalid status code returned 
        try: 
            restCountriesResponse.raise_for_status()
        except:  
            raise requests.exceptions.HTTPError(f'Error retrieving URL {country_url}; Status Code {restCountriesResponse.status_code}')

        #get country name and list of its subdivisions
        countryName = pycountry.countries.get(alpha_2=folder).name
        allSubdivisions = list(pycountry.subdivisions.get(country_code=folder))

        subdivisions = []
        subdivisionNames = []

        #iterate over all files, appending subdivision names and codes to arrays
        for file in allFiles:
            if (file.lower() != "readme.md" and file.lower() != ".ds_store"):     
                if ((isinstance(os.path.splitext(file)[0].split('-')[1], int)) \
                    and os.path.splitext(file)[0].split('-')[1] (len(os.path.splitext(file)[0].split('-')[1]) == 1) \
                    and (1 >= os.path.splitext(file)[0].split('-')[1] <= 9)):
                    subdivisions.append(os.path.splitext(file)[0].split('-')[0] + '-' + '0' + os.path.splitext(file)[0].split('-')[1])
                else:
                    subdivisions.append(os.path.splitext(file)[0]) 
                for subd in allSubdivisions:
                    if (os.path.splitext(file)[0] == subd.code):    
                        subdivisionNames.append(subd.name)
        
        #create dict of subdivison codes and their names           
        subds = dict(zip(subdivisions, subdivisionNames))   
        subds_sorted = {}
        
        #sort subdivision codes/keys in non-natural order
        #e.g: without this sorting for Estonia, some codes were ordered as EE-353, EE-37, EE-39, EE-424
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            '''
            alist.sort(key=natural_keys) sorts in human order
            http://nedbatchelder.com/blog/200712/human_sorting.html
            (See Toothy's implementation in the comments)
            '''
            return [ atoi(c) for c in re.split(r'(\d+)', text) ]

        # subdivisions.sort(key=natural_keys)
# ['ET-AA', 'ET-AF', 'ET-AM', 'ET-BE', 'ET-DD', 'ET-GA', 'ET-HA', 'ET-OR', 'ET-SI', 'ET-SN', 'ET-SO', 'ET-TI']
# ['Addis Ababa', 'Afar', 'Amara', 'Benshangul-Gumaz', 'Dire Dawa', 'Gambela Peoples', 'Harari People', 'Oromia', 'Southern Nations, Nationalities and Peoples', 'Somali', 'Tigrai']

        print(subds)
        print(subdivisions)
        print(subdivisionNames)
        #create new sorted dict of subdivision codes and names
        for sub in subdivisions:

            subds_sorted[sub] = subds[sub]

        #append all subdivision and country info to respective jsons  
        json_data.append(restCountriesResponse.json()[0])
        json_data[countryIndex]["Subdivisions"] = subds_sorted
        json_min_data.append({"Country": countryName, "Code": folder, "Subdivisions": subds_sorted})

        countryIndex+=1 #increment counter

    #write json data with country info to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    #write json data with country info to json min output file
    with open(json_min_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_min_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-countryInputFolder', '--countryInputFolder', type=str, required=False, default="../iso3166-2-icons", help='Input folder of ISO3166 flag icons, ../iso3166-2-icons by default.')
    parser.add_argument('-iso3166Type', '--iso3166Type', type=str, required=False, default="iso3166-2", help='Create ISO3166-1 or ISO3166-2 JSON file, ISO3166-2 by default.')

    #parse input args
    args = parser.parse_args()
    countryInputFolder = args.countryInputFolder
    iso3166Type = args.iso3166Type

    #invalid country folder input
    if not (os.path.isdir(countryInputFolder)):
        raise ValueError(f'Country folder not found at path {countryInputFolder}.')

    #create JSON file for either ISO3166-1 or ISO3166-2
    if (iso3166Type == "iso3166-1"):
        createISO3166_1_Json(countryInputFolder=countryInputFolder)
    else:
        createISO3166_2_Json(countryInputFolder=countryInputFolder)