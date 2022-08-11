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

#initialise logging library 
__version__ = "0.0.1"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-flag-icons/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-flag-icons', getpass.getuser())}


def createISO3166_1_Json(countryFolder="../iso3166-1-icons", jsonFileName="test-1.json"):
    """
    Create JSON file for all ISO3166-1 flag icons, JSON will include the countrys full name,
    2 letter ISO code and full path to its URL in repo. JSON used for importing and displaying
    flags in index.html front-end demo.

    Parameters
    ----------
    : countryFolder (str) 
        filepath to folder containing all ISO3166-1 icons.
    : jsonFileName (str)
        output JSON filename, stored in main repo dir by default. 

    Returns
    -------
    None
    """
    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join("../", jsonFileName)

    #object for storing all json output data
    json_data = []

    #get list of all ISO3166-1 svg files
    allFiles = [f for f in os.listdir(countryFolder) if os.path.isfile(os.path.join(countryFolder, f))]

    #iterate over all svg files in folder, appending country name, code and filepath/url to json
    for country in allFiles:
        #ignore readme file
        if (country.lower() == "readme.md"):
            continue
        countryCode = os.path.splitext(country)[0].upper()
        print(countryCode)
        if (pycountry.countries.get(alpha_2=countryCode) == None):
            countryName = iso3166_.countries_by_alpha2[countryCode.title()].name
        else:
            countryName = pycountry.countries.get(alpha_2=countryCode).name

        # countryName = iso3166_.countries_by_alpha2[countryCode].name
        json_data.append({"Country": countryName, "Code": countryCode, "Flag": os.path.join(countryFolder, country)})

    #write json data to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        

def createISO3166_2_Json(countryFolder="../iso3166-2-icons", jsonFileName="iso3166-2.json"):
    """
    Create JSON file for all ISO3166-2 flag icons. The min JSON file will include the countrys full name,
    2 letter ISO code, list of subdivision code and path to each respective flaf. The other JSON
    will include the last 4 mentioned parameters as well as each country's info from the restcountries
    api. The JSON's will be used for importing and displaying flags in index.html front-end demo.

    Parameters
    ----------
    : countryFolder (str) 
        filepath to folder containing all ISO3166-1 icons.
    : jsonFileName (str)
        output JSON filename, stored in main repo dir by default. 

    Returns
    -------
    None
    """
    #arrays for store all json parameters
    json_data = []
    json_min_data = []

    #path to json file will be in the main repo dir by default
    json_filepath = os.path.join("../", jsonFileName)
    json_min_filepath = os.path.join("../", os.path.splitext(jsonFileName)[0] + '_min' + os.path.splitext(jsonFileName)[1])

    #get list of all ISO3166-2 subfolders
    allFolders = [f for f in os.listdir(countryFolder) if os.path.isdir(os.path.join(countryFolder, f))]

    #iterate over all subdivision folders, getting country and subdivision info, append to json's
    for folder in allFolders:

        #get list of files in country's folder
        allFiles = [f for f in os.listdir(os.path.join(countryFolder, folder)) if os.path.isfile(os.path.join(countryFolder, folder, f))]
        
        #get country info from restcountries api
        restCountriesResponse = requests.get("https://restcountries.com/v3.1/alpha/" + folder, stream=True, headers=USER_AGENT_HEADER)
        #raise error if invalid status code returned 
        try: 
            restCountriesResponse.raise_for_status()
        except:  
            raise requests.exceptions.HTTPError(f'Error retrieving URL {url}; Status Code {restCountriesResponse.status_code}')
        
        #get country name and list of its subdivisions
        countryName = pycountry.countries.get(alpha_2=folder).name
        allSubdivisions = list(pycountry.subdivisions.get(country_code=folder))

        subdivisions = []
        subdivisionNames = []
        
        #iterate over all files, appending subdivision names and codes to arrays
        for file in allFiles:
            if (file.lower() != "readme.md" and file.lower() != ".ds_store"):            
                subdivisions.append(os.path.splitext(file)[0])
                for subd in allSubdivisions:
                    if (os.path.splitext(file)[0] == subd.code):    
                        subdivisionNames.append(subd.name)
        
        #create dict of subdivison codes and their names           
        subds = dict(zip(subdivisions, subdivisionNames))   

        #append all subdivision and country info to respective jsons  
        json_data.append(restCountriesResponse.json())
        json_data.append({"Subdivisions": subds})
        json_min_data.append({"Country": countryName, "Code": folder, "Subdivisions": subds})

    #write json data with country info to json output file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    #write minimal json parameters to output file
    with open(json_min_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_min_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-countryFolder', '--countryFolder', type=str, required=False, default="../iso3166-1-icons", help='Output folder of ISO3166 countrys, ../iso3166-1-icons by default.')
    parser.add_argument('-jsonFileName', '--jsonFileName', type=str, required=False, default="iso3166-1.json", help='Filename of JSON, iso3166-1-icons.json by default.')
    parser.add_argument('-iso3166Type', '--iso3166Type', type=str, required=False, default="iso3166-1", help='Create ISO3166-1 or ISO3166-2 JSON file, ISO3166-1 by default.')

    #parse input args
    args = parser.parse_args()
    countryFolder = args.countryFolder
    jsonFileName = args.jsonFileName
    iso3166Type = args.iso3166Type

    #invalid country folder input
    if not (os.path.isdir(countryFolder)):
        raise ValueError(f'Country folder not found at path {countryFolder}')

    #create JSON file for either ISO3166-1 or ISO3166-2
    if (iso3166Type == "iso3166-1"):
        createISO3166_1_Json(countryFolder=countryFolder, jsonFileName=jsonFileName)
    else:
        createISO3166_2_Json(countryFolder=countryFolder, jsonFileName=jsonFileName)