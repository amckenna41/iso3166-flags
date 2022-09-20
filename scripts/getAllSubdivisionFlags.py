'''
Getting all country subdivision flags from the wiki url:
https://en.wikipedia.org/wiki/Flags_of_country_subdivisions

BeautifulSoup (BS4) is used to web scrape the wiki URL, getting
the URL, filename and respective country for each flag. The custom-built 
pyWikiCommons library is used to download each image using the Wikimedia 
API. Any countries/subdivisions not available on this wiki site are 
retrieved using the getISO3166-2Flags.py script which gets all flags 
from their respective wiki URLs. 

'''
from re import A
import requests
import os
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
      string of country wiki URL to validate

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
    subfolder name specified by pathname with the filename specified by the url arg.

    Parameters
    ----------
    :url : string
      string of country wiki URL.
    :pathname : string
      subfolder within parent folder specified by the country name of URL, used to split up
      each country flags into their respective folders (2 letter country ISO code).
    :country : string
      country name.
    :folder : string
      parent folder name to store country subfolders and country flags.
    :decode : bool
      whether to decode the unicode characters, true by default. 

    Returns 
    -------
    None
    """
    #if path doesn't exist, make that path dir
    if not os.path.isdir(os.path.join(folder, pathname)):
        os.makedirs(os.path.join(folder, pathname))

    #get the file name
    filename = os.path.join(folder, pathname, url.split("/")[-1])

    #if filename too long, just use first 30 characters
    if len(filename) >= 100:
      filename = filename[:30] + '.svg'
    
    #dont download any wiki meta files or corrupted/invalid images
    if os.path.basename(filename) == 'start' or os.path.basename(filename) == 'wikimedia-button.png' or \
      'poweredby_mediawiki' in os.path.basename(filename) or os.path.basename(filename).lower() == 'no_flag' or \
        'Emoji' in os.path.basename(filename):
      return
    
    #decode any unicode characters
    if (decode):
      filename = unquote(filename)

    #remove various chars/substrings from any of the flag names
    char_to_replace = {'Flag_of_the_':'',
                    'flag_of_the_': '',
                    'flag_of_': '',
                    'Flag_of_': '',
                    'flag_': '',
                    'Flag_': '',
                    '_flag': '',
                    '_Flag': '',
                    '-flag': '',
                    '-Flag': '',
                    '(': '',
                    ')': '',
                    ',_': '_',
                    "'": '_',
                    '"': '',
                    '&': 'and',
                    ';': '',
                    '%': '',
                    '!': '',
                    '_-_': '_',
                    '_province': '',
                    '_Province': '',
                    '_municipality': '',
                    '_Municipality': '',
                    '_department': '',
                    '_Department': '',
                    '_prefecture': '',
                    '_Prefecture': '',
                    'bandera_': '',
                    'Bandera_': '',
                    '_governorate': '',
                    'Canton': '',
                    'canton': ''}
    
    #iterate through filename, replacing above chars/substrings with empty space
    for key, value in char_to_replace.items():
        filename = filename.replace(key, value)

    #remove any leading or trailing whitespace, lower case filename
    filename = filename.strip().lower()

    #remove last char if it is an underscore
    if (filename[-1] == '_'):
      filename = filename[0:-1]

    #remove file from start of filename str
    if (filename[:5] == "File/"):
      filename = filename[5:]

    #remove any accented chars from filename
    filename = strip_accents(filename)
    
    #remove '.' from filenames, split file into name and ext first
    name, ext = os.path.basename(os.path.splitext(filename)[0]), os.path.basename(os.path.splitext(filename)[1])
    filename = os.path.join(os.path.dirname(filename), name.replace('.', '') + ext)

    allSubdivision = {}
    allMatches = {}

    #iterate over all subdivision codes, if filename matches any of these codes with high 
    #...percentage using fuzzywuzzy library then change filename to subdivision code
    if ((pycountry.subdivisions.get(country_code=pathname) != None) and 
    (pycountry.subdivisions.get(country_code=pathname) != [])):  #XK = None, EH = []
      for subd in pycountry.subdivisions.get(country_code=pathname): 
        allSubdivision[unquote(strip_accents(subd.name.lower()))] = subd.code
        allMatches[subd.code] = fuzz.ratio(os.path.basename(os.path.splitext(filename)[0]).replace('_', ' ').lower(), unquote(strip_accents(subd.name.lower())))

      #get highest matching subdivision code and its match value
      best_match_code, best_match_val = max(allMatches.items(), key=operator.itemgetter(1))

      #if match likelihood value >0.7 then change filename to best match subdivision code
      if (best_match_val >= 70):
        name, ext = os.path.basename(os.path.splitext(filename)[0]), os.path.basename(os.path.splitext(filename)[1])
        filename = os.path.join(os.path.dirname(filename), best_match_code + ext)

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
  :url : string 
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
        # country = img.findPrevious('h2').find('span').text
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
          
        #skip historical states 
        if (countryCode.lower() == "historical states"):
          continue

        #get wikimedia commons url and download img using pyWikimediaCommons library
        file_url = pyWikiCommons.get_commons_url(img['href'].rsplit('/', 1)[-1])
        download(file_url, countryCode, country, outputFolder)

        downloadedImageCounter+=1 #increment counter

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Downloading all country subdivision flags for Flagle game.')

  parser.add_argument('-output', '--output', type=str, required=False, default="../iso3166-2-icons", help='Output folder path for downloaded ISO3166-2 country SVGs.')

  #parse input args
  args = parser.parse_args()
  outputFolder = args.output

  #start counter
  start = time.time()

  print('###################################################################################################')
  print('Downloading subdivision flags from URL: {} to output folder {}\n'.format(URL, outputFolder))
  
  #download all images from subdivision URL
  download_all_images(outputFolder)

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
  # for country_ in list(pycountry.countries):
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

      print(os.path.basename(folder))
      #generate readme.md for each country subfolder in output folder      
      createReadMe(country, os.path.basename(folder), URL, outputFolder)

  #stop counter, calculate elapsed time
  elapsed = (time.time() - start)
  print('#######################################################\n')
  print('Elapsed execution time: {:.2f} seconds.\n'.format(elapsed))
  
