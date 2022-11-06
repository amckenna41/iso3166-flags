# Scripts for downloading all ISO3166-2 country subdivision flags

[![pytest](https://github.com/amckenna41/iso3166-flag-icons/workflows/iso3166_workflow/badge.svg)](https://github.com/amckenna41/iso3166-flag-icons/actions/workflows/iso3166_workflow.yml)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/pySAR/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Build](https://img.shields.io/github/workflow/status/amckenna41/pySAR/Deploy%20to%20PyPI%20%F0%9F%93%A6)](https://github.com/amckenna41/pySAR/actions)
<!-- [![CircleCI](https://circleci.com/gh/amckenna41/pySAR.svg?style=svg&circle-token=d860bb64668be19d44f106841b80eb47a8b7e7e8)](https://app.circleci.com/pipelines/github/amckenna41/pySAR) -->
[![codecov](https://codecov.io/gh/amckenna41/iso3166-flag-icons/branch/master/graph/badge.svg?token="")](https://codecov.io/gh/amckenna41/iso3166-flag-icons)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons)
[![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons)


Purpose
-------
After browsing through the likes of GitHub and Kaggle I found out that there wasn't any solid and reliable dataset for ISO3166-2 icons. There existed several repos and datasets for the ISO3166-1 flags, mainly due to their being a much smaller amount (~270) compared to the X that are available in the ISO3166-2 folder of this repo. 
Several scripts were required to automate the collection, downloading and cleaning of the thousands of ISO3166-2 flag images, generating a pipeline that starts with a web-scraping function and ends with the creation of the custom CSS and JSON files also present in the repo.

Note the `jquery-jvectormap-2.0.5.js` and `jquery-jvectormap-2.0.5.css` files are only required for the interactive map demo of the repo found [here](https://amckenna41.github.io/iso3166-flag-icons-website/).

The exact purpose of each script can be seen below, as well as in the comments of each file:
* `getAllSubdivisionFlags.py` - downloading all ISO3166-2 subdivision flags from the main subdivisions wiki (https://en.wikipedia.org/wiki/Flags_of_country_subdivisions) as well as using country's respective wiki URL's. 
* `generateReadMe.py` - create README file for each ISO3166-2 subfolder, listing all the subdivisions per country.
* `generateCSS.py` - create CSS files with respective CSS selectors/classes for both ISO3166-2 and ISO3166-2 flag icons.
* `generateJSON.py` - create JSON files of flag files, their name and ISO code for both ISO3166-1 and ISO3166-2 folders. 
* `iso3166_.py` - list of all ISO3166 country names, alpha2 and alpha3 codes.
* `mapMarkers.js` - script for adding smaller countries/jurisdictions as markers to the jsVectorMaps.
* `jquery-jvectormap-2.0.5.css` - styling for jvectormap interactive maps.
* `jquery-jvectormap-2.0.5.js` - jvectormap library source code to built interactive maps.
* `svgCompress.sh` - script for compressing folder of image flags in SVG format.

Requirements
------------

* [Python][python] >= 3.6
* [requests][requests] >= 1.16.0
* [pandas][pandas] >= 1.4.3
* [tqdm][tqdm] >= 4.55.0
* [beautifulsoup4][beautifulsoup4] >= 4.10.0
* [scour][scour] >= 0.38.2
* [pycountry][pycountry] >= 22.3.5
* [emoji-country-flag][emoji-country-flag]>= 1.3.0
* [fuzzywuzzy][fuzzywuzzy] >= 0.18.0
* [pyWikiCommons][pyWikiCommons] >= 0.0.1

Usage
-----

## Download all ISO3166-2 subdivision flags

```bash
python3 getAllSubdivisionFlags.py --output="../iso3166-2-icons" 

--output: output folder to downloaded flag files
--url_csv: using default value of iso3166-2_urls.csv
--no_flags_csv: using default value of noISO3166-2Flags.csv
```

## Compress all SVG flag icon files in output folder

```bash
./svgCompress.sh --input="../iso3166-2-icons/" --output="../output/" --filesize=50

--input: input folder of SVG files to compress
--output: output folder to store compressed SVG files
--filesize_threshold: all SVG files above this threshold will go through the compression algorithm. 
```

<strong>After execution of the ./svgCompress.sh script, the iso3166-2-icons dir was compressed from XMB -> YMB.</strong>

## Create CSS files for both ISO3166-1 and ISO3166-2 icons

```bash
python3 generateCSS.py --countryFolder="../iso3166-1-icons" --cssFileName="iso3166-1-icons.css" --iso3166Type="iso3166-1"
```

## Create ISO3166-1 or ISO3166-2 JSON files containing all flag and subdivision info per country/jurisdiction

```bash
python3 generateJSON.py --countryFolder="" --jsonFileName="" --iso3166Type=""
```

## Create README files for each ISO3166-2 country in iso3166-2-icons dir, listing contents of dir and subdivision info

```bash
python3 generateReadme.py --country
```

Tests
-----
Several Python test scripts were created using (unittest)[https://docs.python.org/3/library/unittest.html] framework. These tests test the full pipeline from getting the flags via web-scraping to exporting the flag & country info to json. 
To run all tests, from the <i>scripts</i> repo folder run:
```
python3 -m unittest discover -v
```

To run tests for specific module, from the main <i>scripts</i> repo folder run:
```
python -m unittest tests.MODULE_NAME -v
-v : verbose output

```

<!-- 3511 seconds total-->
