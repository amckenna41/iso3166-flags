'''
Get ISO3166-2 Flag icons according to CSV of countrys and their respective URLs using
the BS4 web scraping library. 

BeautifulSoup (BS4) is used to web scrape the wiki URL, getting
the URL, filename and respective country for each flag. The custom-built 
pyWikiCommons library is used to download each image using the Wikimedia 
API. This script is executed after the getAllSubdivisionFlags.py script which 
uses the wiki url https://en.wikipedia.org/wiki/Flags_of_country_subdivisions to
download most country subdivisions that are available on it. 

'''

import requests
import os
import pandas as pd
import argparse
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, unquote
import unicodedata
from pyWikiCommons import pyWikiCommons

from generateReadMe import *
from getAllSubdivisionFlags import *
import iso3166_

#initialise logging library 
__version__ = "0.0.1"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-flag-icons/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-flags-icons', getpass.getuser())}
#counter for num of total images downloaded
downloadedImagesCounter = 0

def get_all_images_from_url(url, outputFolder="", country="", iso_code=""):
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
  #...using download function from the getAllSubdivisionFlags.py module
  for img in all_imgs:
    if (img.has_attr('href')):
      if (img['href'].startswith('/wiki/File:')):
        file_url = pyWikiCommons.get_commons_url(img['href'].rsplit('/', 1)[-1])
        download(file_url, iso_code, country, outputFolder)
        # downloadedImageCounter+=1

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Downloading all country subdivision flags for Flagle game.')

    parser.add_argument('-output', '--output', type=str, required=False, default="../iso3166-2-icons-test", help='Output folder path for downloaded country SVGs')
    parser.add_argument('-country', '--country', type=str, required=False, default="", help='Country name')
    parser.add_argument('-url_csv', '--url_csv', type=str, required=False, default="iso3166-2_urls.csv", help='CSV of countrys wiki URLs')

    #parse input args
    args = parser.parse_args()
    outputFolder = args.output
    countryInput = args.country
    url_csv = args.url_csv
      
    url_csv = "test_urls.csv"
    #import csv of countrys and their wiki urls
    country_csv = pd.read_csv(os.path.join("iso3166-files", url_csv))
    
    #convert 2 columns of wiki into dict
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

    print('#######################################################')
    print('Downloading flags for {} countries...'.format(len(country_dict)))
    
    #start counter
    start = time.time()

    #iterate over all countries and associated urls and download all imgs from it
    for country_, url_ in country_dict.items():
      #get ISO 2 letter-code of country; if not found, folder will be the country name
      if (iso3166_.countries_by_name.get(country_.title()) is None): 
        iso_code = country_
      else:
        iso_code = iso3166_.countries_by_name[country_.title()].alpha2

      print(f'\n###### {country_} ({iso_code}): {url_} ######')

      #download all images from wiki url, store in output folder in iso_code subdir
      get_all_images_from_url(url_, outputFolder, country_, iso_code)

      #generate readme of all images in subdir of output folder
      createReadMe(country_, iso_code, url_, outputFolder)
      
      print('Downloaded {} images to folder {}'.format(downloadedImagesCounter, outputFolder))
      downloadedImagesCounter = 0

    #stop counter, calculate elapsed time
    elapsed = (time.time() - start)
    print('#######################################################\n')
    print('Elapsed execution time: {:.2f} seconds.\n'.format(elapsed))