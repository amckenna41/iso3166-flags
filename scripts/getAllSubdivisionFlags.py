import requests
import os
from tqdm import tqdm
import argparse
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import subprocess
import unicodedata
import iso3166_

#url and headers for user agent
URL = "https://en.wikipedia.org/wiki/Flags_of_country_subdivisions"
HEADERS = {'User-Agent': 'Flagle/0.0 (https://github.com/amckenna41; mckenna45678@hotmail.co.uk)'}

#add closeness function for ISO3166 code

def is_valid(url):
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

def download(url, pathname, country, folder="../countries"):
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

    Returns 
    -------
    None
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(os.path.join(folder, pathname)):
        os.makedirs(os.path.join(folder, pathname))

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True, headers=HEADERS)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(folder, pathname, url.split("/")[-1])

    #if file exists then return from func
    if os.path.isfile(filename):
      return

    #if filename too long, just use first 30 characters
    if len(filename) >= 100:
      filename = filename[:30] + '.svg.png'
    
    #dont download any wiki meta files
    if os.path.basename(filename) == 'start' or os.path.basename(filename) == 'wikimedia-button.png' or 'poweredby_mediawiki' in os.path.basename(filename):
      return

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"{country} ({pathname}): Downloading {os.path.basename(filename)} to filepath {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    #write country img data to the file
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def download_all_images(outputFolder, url=None):
  """
  Download all images from subdivision URL.

  Parameters
  ----------
  :outputFolder : string
    pathname of folder to store the country flags in.
  :url : string (default=None)
    url of wiki to download the country/subdivision flags,
    https://en.wikipedia.org/wiki/Flags_of_country_subdivisions used by default.

  Returns 
  -------
  None
  """
  #if no url arg input, use default wiki URL
  if (url is None) or (url == ""):
    url = URL

  #initialise BS4 object
  soup = bs(requests.get(url).content, "html.parser")
  
  #get all divs on wiki URL
  all_divs = soup.find_all("a", {"class": "image"})

  country = ""
  countryCode = ""

  #convert accented chars to normal via unicode decode
  def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                    if unicodedata.category(c) != 'Mn')
            
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

        #get ISO 2 letter-code of country, if not found folder will be the country name
        if (iso3166_.countries_by_name.get(country.upper()) is None): 
          countryCode = country
        else:
          countryCode = iso3166_.countries_by_name[country.upper()].alpha2
        
        #initialise bs4 object with url of flag img
        flag_wiki_soup = bs(requests.get('https://en.wikipedia.org' + img['href']).content, "html.parser")

        #iterate over all 'a' tags, finding and downloading the original svg img tag 
        for tag in flag_wiki_soup.findAll('a'):
          if (tag.text.lower() == 'original file'):
            download('https:' + tag['href'], countryCode, country, outputFolder)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Downloading all country subdivision flags for Flagle game.')

  parser.add_argument('-output', '--output', type=str, required=False, default="../countries", help='Output folder path for downloaded country SVGs')

  #parse input args
  args = parser.parse_args()
  outputFolder = args.output

  #download all images from subdivision URL
  download_all_images(outputFolder)

  # val = subprocess.check_call("./svgCompress.sh '%f'" % "test", shell=True)
  # subprocess.run(["chmod", "+x", "/content/svgCompress.sh"])
  # rc = subprocess.call("/content/svgCompress.sh")

# def download_all_images(url):
#     """
#     """
#     if url is None:
#       url = URL

#     soup = bs(requests.get(url).content, "html.parser")
#     urls = []
#     for img in tqdm(soup.find_all("img"), "Extracting images"):
#         img_url = img.attrs.get("src")
#         # img_url = img.attrs.get("data-src")
#         if not img_url:
#             # if img does not contain src attribute, just skip
#             continue
#         # make the URL absolute by joining domain with the URL that is just extracted
#         img_url = urljoin(url, img_url)
#         # remove URLs like '/hsts-pixel.gif?c=3.2.5'
#         try:
#             pos = img_url.index("?")
#             img_url = img_url[:pos]
#         except ValueError:
#             pass
#         # finally, if the url is valid
#         if is_valid(img_url):
#             urls.append(img_url)
#     return urls

