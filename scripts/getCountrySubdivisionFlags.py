from getAllSubdivisionFlags import *
import pandas as pd
import iso3166_
import time
import subprocess

def get_all_images_from_url(selectedURL=None, outputFolder="", country=""):
  """
  Parameters
  ----------
  :selectedURL : string 
    URL of wiki site to download images from.
  :outputFolder : string
    pathname of output folder to store country folders and files.
  :country : string
    name of country.

  Returns
  -------
  None
  """
  #raise exception if invalid URL not input
  if (selectedURL is None) or not isinstance(selectedURL, str):
      raise ValueError('Invalid URL input: {}'.format(selectedURL))

  #get ISO 2 letter-code of country, if not found folder will be the country name
  if (iso3166_.countries_by_name.get(country.upper()) is None): 
    iso_code = country
  else:
    iso_code = iso3166_.countries_by_name[country.upper()].alpha2
  
  #if output folder of country exists then break 
  if (os.path.isdir(os.path.join(outputFolder, iso_code))):
    return

  #initialise bs4 object from url
  soup = bs(requests.get(selectedURL).content, "html.parser")

  #get all image anchor tags on page
  all_imgs = soup.find_all("a", {"class": "image"})

  #iterate over all 'a' tags, finding and downloading the original svg img tag 
  for img in all_imgs:
    if (img.has_attr('href')):
      if (img['href'].startswith('/wiki/File:')):
        flag_wiki_soup = bs(requests.get('https://en.wikipedia.org' + img['href']).content, "html.parser")
        for tag in flag_wiki_soup.findAll('a'):
          if (tag.text.lower() == 'original file'):
            download('https:' + tag['href'], iso_code, country, outputFolder)

if __name__ == '__main__':

    #create argument parser object and add arguments
    parser = argparse.ArgumentParser(description='Downloading all country subdivision flags for Flagle game, getting flags from countrys individual wiki page.')
    parser.add_argument('-country', '--country', type=str, required=False, default="all", help='Name of country/subdivision.')
    parser.add_argument('-url', '--url', type=str, required=False, default="", help='URL of wiki to download countrys flags from, if empty then all images from all URLs will be downloaded.')
    parser.add_argument('-output', '--output', type=str, required=False, default="countries", help='Output folder path for downloaded country SVGs')

    #parse input args
    args = parser.parse_args()

    country = args.country
    url = args.url
    output = args.output
    output = "test"

    #import csv of countries and their wiki URLs
    country_csv = pd.read_csv('countryURLs.csv')
    url_dict = dict(zip(list(country_csv['Country']), list(country_csv['URL'])))

    print('#######################################################')

    if (url == ""):
        print('Downloading flags for {} countries...'.format(len(url_dict)))
    else:
        print('Downloading flags for country {} and URL {} ...'.format(country, url))

    #start counter
    start = time.time()

    #iterate over all countries and associated urls and download all imgs from it
    for country_, url_ in url_dict.items():
      print(f'###### {country_} ######')
      get_all_images_from_url(url_, output, country_)

    #stop counter, calculate elapsed time
    elapsed = (time.time() - start)
    print('#######################################################')
    print('Elapsed Training Time: {:.2f} seconds.\n'.format(elapsed))

    #call SVG compression script on downloaded flags
    # subprocess.call(['./svgCompress.sh', output, 'outputs'])
    
    #execute SVG compression script to 
    print('#######################################################')
