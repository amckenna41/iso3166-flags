'''
Script for automating the download of all country subdivisions.
The first step in the pipeline is to download all available subdivisions 
from the wiki url: https://en.wikipedia.org/wiki/Flags_of_country_subdivisions .
This URL contains many subdivision flags for countrys, but those that are not 
available are separately downloaded using their respective wiki URL's, listed in
the /iso3166-files/iso3166-2_urls.csv file.

The pipeline includes the web-scraping of the URL's, downloading of the images,
creating the output folders, assigning the correct ISO3166-2 subdivision names 
to the downloaded images and generating a README file for each country's respective
directory containing a description of the country and its subdivisions.

BeautifulSoup (BS4) is used to web scrape the wiki URL, getting
the URL, filename and respective country for each flag. The custom-built 
pyWikiCommons library is used to download each image using the Wikimedia 
API (https://pypi.org/project/pyWikiCommons/)
'''
from re import A
import requests
import os
import pandas as pd
from tqdm import tqdm
import argparse
import time
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, unquote
import unicodedata
import logging 
import getpass
from fuzzywuzzy import fuzz
import operator
import pycountry
from pyWikiCommons import pyWikiCommons

from generateReadMe import *
import iso3166_

#initialise logging library 
__version__ = "0.0.1"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-flag-icons/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-flag-icons', getpass.getuser())}
#wiki URL which contains most countrys and their associated subdivisions
URL = "https://en.wikipedia.org/wiki/Flags_of_country_subdivisions"

#counting the number of images downloaded
downloadedImageCounter = 0

def valid_url(url):
    """
    Checks whether `url` is a valid URL.

    Parameters
    ----------
    :url : string 
      string of country wiki URL to validate.

    Returns
    -------
    :bool : bool
      boolean of if URL is valid or not.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#convert accented chars to normal via unicode decode
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                    if unicodedata.category(c) != 'Mn')
                  
def download(url, pathname, country, folder="../countries", decode=True):
    """
    Download SVG file from URL, save to parent folder specified by folder arg, with the 
    subfolder name specified by pathname and the filename specified by the url arg.
    Parse filename, removing any unwanted chars/strings/numbers etc, decode any unicode
    chars, remove any accents from name and match flag to the country's specific 
    ISO3166-2 subdivision code.

    Parameters
    ----------
    :url : string
        string of country wiki URL.
    :pathname : string
        subfolder within parent folder specified by the country name of URL, used to split up
        each country flags into their respective folders (2 letter country ISO3166-2 code).
    :country : string
        country name.
    :folder : string (default="../countries")
        parent folder name to store country subfolders and country flags.
    :decode : bool (default=True)
        whether to decode the unicode characters, true by default. 

    Returns 
    -------
    None
    """
    #if path doesn't exist, make that path dir
    if not os.path.isdir(os.path.join(folder, pathname)):
        os.makedirs(os.path.join(folder, pathname))

    #get the file name from url
    filename = url.split("/")[-1].lower()

    #if filename too long, just use first 30 characters
    if len(filename) >= 100:
        filename = filename[:30] + '.svg'
    
    #dont download any wiki meta files or corrupted/invalid images
    if filename == 'start' or filename == 'wikimedia-button.png' or filename == "symbol_portal_class.svg":
        return

    #skip non-flag files if contain any of the below invalid strings
    skip_filenames = ['poweredby_mediawiki', 'no_flag', 'Emoji', 'proposal',
        'ensign', 'police', 'air_force', 'military', 'alternative',
        'president', 'people', 'maritime', 'coast_guard', 'university', 
        'proposed', 'royal_standard', 'commander', 'army', 'presidential',
        'governor', 'ministry', 'airport', 'border_force', 'customs' 'burgee',
        'navy', 'royal_banner', 'unofficial', country.lower()
    ]

    #skip downloading file if file contains any strings in array
    skip = False 
    for string in skip_filenames:
        if (string in filename):
            skip = True
            break
    if (skip):
        return
        
    #decode any unicode characters
    if (decode):
        filename = unquote(filename)

    #remove and or replace various chars/substrings from any of the flag names    
    char_to_replace = ['flag_of_the_', 'flag_of_', 'flag_', '_flag', '-flag', '(', ')', '"', ';',
                    '%', '!', '_province', '_municipality', '_department', '_prefecture',
                    'bandera_', '_governorate', 'canton', 'File/', 'File:', '_region', '_state', 
                    'de_la_provincia_', 'provincia', 'bandeira', 'bandeira_de_provincia_',
                    'bandeira_provincia_', 'province_de']

    char_to_replace_ = {',_': '_',
                        "'": '_',
                        '&': 'and',
                        '_-_': '_',
                        '__': '_'}

    #remove any leading or trailing whitespace, lower case filename
    filename = filename.strip().lower()

    #iterate through filename, replacing above chars/substrings with empty space
    for char in char_to_replace:
        filename = filename.replace(char, '')

    #iterate through filename, replacing above chars/substrings with value in dict
    for key, value in char_to_replace_.items():
        filename = filename.replace(key, value)

    #remove first and last char if it is an underscore
    if (filename[0] == '_'):
        filename = filename[1:]

    if (filename[-1] == '_'):
        filename = filename[0:-1]

    #remove any accented chars from filename
    filename = strip_accents(filename)
    
    #remove '.' from filenames, split file into name and ext first
    name, ext = os.path.splitext(filename)[0], os.path.splitext(filename)[1]
    filename = os.path.join(os.path.dirname(filename), name.replace('.', '') + ext)

    allSubdivision = {}
    allMatches = {}

    #iterate over all subdivision codes, if filename matches any of these codes with high 
    #...percentage using fuzzywuzzy library then change filename to subdivision code
    if ((pycountry.subdivisions.get(country_code=pathname) != None) and 
        (pycountry.subdivisions.get(country_code=pathname) != [])):  #XK = None, EH = []
        for subd in pycountry.subdivisions.get(country_code=pathname): 
            allSubdivision[unquote(strip_accents(subd.name.lower()))] = subd.code
            allMatches[subd.code] = fuzz.ratio(os.path.splitext(filename)[0].replace('_', ' ').lower(), unquote(strip_accents(subd.name.lower())))

    #validate there exists any matching subdivisions
    if (allMatches):
        #get highest matching subdivision code and its match value
        best_match_code, best_match_val = max(allMatches.items(), key=operator.itemgetter(1))

        #if match likelihood value >0.75 then change filename to best match subdivision code
        if (best_match_val >= 75):
            name, ext = os.path.splitext(filename)[0], os.path.splitext(filename)[1]
            filename = os.path.join(os.path.dirname(filename), best_match_code + ext)

    #get filepath to filename
    filename = os.path.join(folder, pathname, filename)

    #if filename exists then skip and return from func
    if os.path.isfile(filename):
        return

    #download the body of response by chunk, not all at once 
    #...pass in custom user-agent as header to not recieve 403 error
    response = requests.get(url, stream=True, headers=USER_AGENT_HEADER)

    #raise error if invalid status code returned 
    try: 
        response.raise_for_status()
    except:  
        raise requests.exceptions.HTTPError(f'Error retrieving URL {url}; Status Code {response.status_code}')

    #get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    #progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"{country} ({pathname}): Downloading {os.path.basename(filename)} to filepath {filename}", \
    total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    #write country img data to the file
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def download_all_images(outputFolder, url=""):
    """
    Download all images from subdivision wiki URL.

    Parameters
    ----------
    :outputFolder : string
        pathname of folder to store the country flags in.
    :url : string (default="")
        url of wiki to download the country/subdivision flags,
        https://en.wikipedia.org/wiki/Flags_of_country_subdivisions used by default.

    Returns 
    -------
    None
    """
    #make counter var global
    global downloadedImageCounter

    #if no url arg input, use default wiki URL
    if (url is None) or (url == ""):
        url = URL
    else:
        if (url is None) or not isinstance(url, str) or not (valid_url(url)):
            raise ValueError('Invalid URL input: {}.'.format(url))

    #initialise BS4 object
    soup = bs(requests.get(url).content, "html.parser")
    
    #get all divs on wiki URL
    all_divs = soup.find_all("a", {"class": "image"})

    country = ""
    countryCode = ""
                
    #iterate over all divs, download all images to its respective country folder
    for img in all_divs:
        if (img.has_attr('href')):
            if (img['href'].startswith('/wiki/File:')):
                
                country = img.findPrevious('h2').findAll('span')[0].text

                #if country name not found in 1st span then go to 2nd
                if (country == ""):
                    country = img.findPrevious('h2').findAll('span')[1].text
                
                #remove any accented letters from country name
                country = strip_accents(country)

                #get ISO 2 letter-code of country, if not found, folder will be the country name
                if (iso3166_.countries_by_name.get(country.title()) is None): 
                    countryCode = country
                else:
                    countryCode = iso3166_.countries_by_name[country.title()].alpha2
                
                #skip historical states and any countries that have no subdivision flags
                if (countryCode.lower() == "historical states" or countryCode in no_flags_list):
                    continue

                #get wikimedia commons url and download img using pyWikiCommons library
                file_url = pyWikiCommons.get_commons_url(img['href'].rsplit('/', 1)[-1])
                download(file_url, countryCode, country, outputFolder)

                downloadedImageCounter+=1 #increment counter


def get_all_images_from_url(url, outputFolder, country, iso_code):
    """
    Parameters
    ----------
    :url : string 
        URL of wiki site to download images from.
    :outputFolder : string 
        pathname of output folder to store country folders and files.
    :country : string
        name of country.
    :iso_code : string
        2 letter ISO code of selected country.

    Returns
    -------
    None
    """
    global downloadedImageCounter #make image counter global

    #raise exception if invalid URL not input
    if (url is None) or not isinstance(url, str) or not (valid_url(url)):
        raise ValueError('Invalid URL input: {}.'.format(url))

    #initialise bs4 object from url
    soup = bs(requests.get(url).content, "html.parser")

    #get all image anchor tags on page
    all_imgs = soup.find_all("a", {"class": "image"})
    
    #iterate over all 'a' tags, finding and downloading the original svg img tag
    #...using download function
    for img in all_imgs:
        if (img.has_attr('href')):
            if (img['href'].startswith('/wiki/File:')):
                file_url = pyWikiCommons.get_commons_url(img['href'].rsplit('/', 1)[-1])
                download(file_url, iso_code, country, outputFolder)
                downloadedImageCounter+=1

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Downloading all ISO3166-2 flags.')

    parser.add_argument('-output', '--output', type=str, required=False, default="../iso3166-2-icons-test-2", help='Output folder path for downloaded ISO3166-2 country SVGs.')
    parser.add_argument('-countryInput', '--countryInput', type=str, required=False, default="", help='Country name if downloading single country from URL.')
    parser.add_argument('-url_csv', '--url_csv', type=str, required=False, default="iso3166-2_urls.csv", help='CSV of countrys wiki URLs')
    parser.add_argument('-no_flags_csv', '--no_flags_csv', type=str, required=False, default="noISO3166-2Flags.csv", help='CSV of all countrys and their ISO codes that have no associated ISO3166-2 flags.')

    #parse input args
    args = parser.parse_args()
    outputFolder = args.output
    countryInput = args.countryInput
    url_csv = args.url_csv
    no_flags_csv = args.no_flags_csv
    
    #import csv of countrys and their wiki urls
    if (os.path.isfile(url_csv)):
        pass
    elif (os.path.isfile(os.path.join("iso3166-files", url_csv))):
        url_csv = os.path.join("iso3166-files", url_csv)
    else:
        raise OSError("Invalid countrys url csv filepath: {}".format(url_csv))

    country_csv = pd.read_csv(url_csv)

    #import csv of a list of countries/jurisdictions that have no subdivision flags
    if (os.path.isfile(no_flags_csv)):
        pass
    elif (os.path.isfile(os.path.join("iso3166-files", no_flags_csv))):
        no_flags_csv = os.path.join("iso3166-files", no_flags_csv)
    else:
        raise OSError("Invalid no ISO3166-2 flags csv filepath: {}".format(no_flags_csv)) 
    
    #create output folder if doesnt exist
    if not(os.path.isdir(outputFolder)):
        os.makedirs(outputFolder)

    #convert csv to dict of {Code: Country}, make list of no flags global,
    #...list used to ensure countries with no flags aren't passed to the download functions
    global no_flags_list
    no_flags_csv = pd.read_csv(no_flags_csv)
    no_flags_dict = dict(zip(list(no_flags_csv['Code']), list(no_flags_csv['Country'])))
    no_flags_list = list(no_flags_dict.keys())

    #convert country and URL columns of wiki csv into dicts
    url_dict = dict(zip(list(country_csv['Country']), list(country_csv['URL'])))
    all_countries = list(map(lambda x: [x.lower()], url_dict.keys()))

    #validate valid country name input as arg, get country dict of countries and their urls
    if (countryInput != ""):
        if ([countryInput] not in all_countries):
            raise ValueError('Invalid country name input {}.').format(countryInput)
        else:
            country_dict = {countryInput: url_dict[countryInput]}
    else:
        country_dict = url_dict

    #start counter
    start = time.time()

    print('###################################################################################################')
    print('Downloading subdivision flags from URL: {} to output folder {}\n'.format(URL, outputFolder))
    
    #download all images from wiki subdivision URL
    # download_all_images(outputFolder)

    print('#######################################################')
    print('Downloading flags for {} countries...'.format(len(country_dict)))

    #iterate over all countries and associated urls and download all imgs from it
    for country_, url_ in country_dict.items():
        
      #split urls into list if more than one in dict
      url_ = url_.strip().split(',')

      #get ISO 2 letter-code of country; if not found, folder will be the country name
      if (iso3166_.countries_by_name.get(country_.title()) is None): 
        iso_code = country_
      else:
        iso_code = iso3166_.countries_by_name[country_.title()].alpha2
      
      #download all images from wiki url, store in output folder in iso_code subdir,
      #...skip downloading func for countrys with no associated subdivision flags
      for urls in url_:
        print(f'\n###### {country_} ({iso_code}): {urls} ######')
        if (iso_code not in no_flags_list):   
            get_all_images_from_url(urls.strip(), outputFolder, country_, iso_code)
            print('\n')
            
      print('Downloaded {} images to folder {}\n'.format(downloadedImageCounter, outputFolder))
      downloadedImageCounter = 0

    print('###################################################################################################')
    print('Downloaded {} images to folder {}'.format(downloadedImageCounter, outputFolder))

    #get list of all folder names in outut directory
    if (os.path.isdir(outputFolder)):
        allFolders = [ f.path for f in os.scandir(outputFolder) if f.is_dir() ]
    else:
        raise OSError('Output folder {} does not exist.'.format(outputFolder))
    
    all_codes = []

    #get list of all iso codes
    for code in iso3166_.countries:
        all_codes.append(code)

    #get country name for all iso code subfolders
    for folder in allFolders:
        if (os.path.basename(folder) in all_codes):
            country = iso3166_.countries[os.path.basename(folder)].name
        else:
            country = os.path.basename(folder)

        #skip historical states 
        if (country.lower() == "historical states"):
            continue

        #generate readme.md for each country subfolder in output folder      
        createReadMe(country, os.path.basename(folder), URL, outputFolder)

    #stop counter, calculate elapsed time
    elapsed = (time.time() - start)

    print('#######################################################\n')
    print('Elapsed execution time: {:.2f} seconds.\n'.format(elapsed))