# Repository of all ISO3166-1 and ISO3166-2 Flags 

[![pytest](https://github.com/amckenna41/iso3166-flag-icons/workflows/Building%20and%20Testing%20iso3166-flag-icons/badge.svg)](https://github.com/amckenna41/iso3166-flag-icons/actions?query=workflowBuilding%20and%20Testing%20iso3166-flag-icons)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons)
[![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-flag-icons)](https://github.com/iso3166-flag-icons)

> A comprehensive library of ISO3166-1 & ISO3166-2 country/subdivision codes and their corresponding flag icons in SVG format. View demo [here](https://amckenna41.github.io/iso3166-flag-icons-website/).

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="400" width="700"/>
</p>

iso3166-flag-icons is a comprehensive repository of all ISO 3166-1 and ISO 3166-2 flag icons according to the International Organisation for Standard that defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). The repo contains <em>266</em> ISO3166-1 alpha-2 flag icons and over <em>3200</em> ISO3166-2 flags. <br> 

The <b>ISO 3166-1</b> icons are those of the names of countries and their subdivisions that can be broken into three sets of country codes:
* ISO 3166-1 alpha-2 – two-letter country codes which are the most widely used of the three, and used most prominently for the Internet's country code top-level domains (with a few exceptions).
* ISO 3166-1 alpha-3 – three-letter country codes which allow a better visual association between the codes and the country names than the alpha-2 codes.
* ISO 3166-1 numeric – three-digit country codes which are identical to those developed and maintained by the United Nations Statistics Division, with the advantage of script (writing system) independence, and hence useful for people or systems using non-Latin scripts.

The <b>ISO 3166-2</b> icons are those of the names of countries and their subdivisions – Part 2: Country subdivision code, defines codes for the names of the principal subdivisions (e.g., provinces, states, departments, regions) of all countries coded in ISO 3166-1 [[2]](#references). <br>

The <b>ISO 3166-3</b> icons are those of countries and their subdivisions – Part 3: Code for formerly used names of countries, defines codes for country names which have been deleted from ISO 3166-1 since its first publication in 1974.

Table of Contents
-----------------

  * [Motivation](#motivation)
  * [Usage](#usage)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Directory Folders](#foldersandfiles)
  * [Open Issues](#Issues)
  * [Contact](#contact)
  * [License](#license)
  * [References](#references)

Motivation
----------
The main motivation behind this project was to integrate additional flag icons into my custom-built web-app <b>Flagle</b> (https://flagle.vercel.app/). This daily worldle-inspired game generates a new flag from around the world each day, consisting of flags of countries, territories and everywhere in between. <br>

After searching around, it was fairly straightforward to find a repo with ISO 3166-1 flags, an example being [here][flag-icons-repo] but there didn't seem to be any single repo/dataset of all ISO 3166-2 subdivision flags, hence I decided to make one from scratch. <br>

Installation
------------
<strong>A zipped folder of all ISO 3166-1 OR ISO 3166-2 flag icons are available to download in the /downloads folder of the repo.</strong>

The whole project can be cloned from git:
```
git clone https://github.com/amckenna41/iso3166-flag-icons.git
```

The ISO 3166-1 and ISO 3166-2 are also split into branches and be downloaded seperately:
```
git clone -b iso3166-1-icons https://github.com/amckenna41/iso3166-flag-icons.git 
OR
git clone -b iso3166-2-icons https://github.com/amckenna41/iso3166-flag-icons.git 
```

Install via npm or yarn (<b><i>not implemented yet</i></b>):
```
npm install --dev iso3166-flag-icons

yarn add --dev iso3166-flag-icons
```

Usage
-----

The flags can be implemented in-line by referencing the CSS class of the respective flag using the ISO 3166-1 or ISO 3166-2 CSS file. For ISO 3166-1 icons add the classes `.fi` and `.fi-xx` (where `xx` is the ISO 3166-1-alpha-2 code [[5]](#references) of a country) to an empty `<span>`. To add a squared version flag then additionally add the class `fis`. Example: 

```html
<span class="fi fi-ad"></span> <span class="fi fi-ad fis"></span>
```

For ISO 3166-2 icons add the classes `.fi` and `.fi-xx-yy` (where `xx` is the ISO 3166-1-alpha-2 code [[2]](#references) of a country and `yy` is the ISO 3166-2 code, both in lower-case) to an empty `<span>`. For example to import the flag for the Canillo Parish of Andorra:

```html
<span class="fi fi-ad-02"></span> <span class="fi fi-ad-02 fis"></span>
```

Folders and files
-----------------

* `/iso3166-1-icons` - flags of all country/territories/subdivisions according to the ISO 3166-1 standard [[5]](#references).
* `/iso3166-2-icons` - flags of all subdivisions within countries/territories according to the ISO 3166-2 standard [[2]](#references).
* `/scripts` - various Python and bash scripts created for downloading and compressing all the required flag SVG files for both the ISO 3166-1 and ISO 3166-2 icons, as well as scripts for creating the json, CSS and readme files.
* `/downloads` - directory of zipped iso3166-1 and iso3166-2 flag icons files.
* `/css` - css scripts for integrating the flags into front-end projects.
* `index.html` - front-end demo for iso3166-flag-icons repo.
* `iso3166-1.json` - json containing all ISO 3166-1 country names, 2 letter codes and relative path to flag icon in repo.
* `iso3166-2.json` - json containing all ISO 3166-2 country names, 2 letter codes, all subdivision codes and common names as well as all info pulled per country via the restcountries api (https://restcountries.com/). 
* `iso3166-2-min.json` - minimised json containing all ISO 3166-2 country names, 2 letter codes and all subdivision codes and common names.

Issues
------
Due to the nature of the methodology for getting the ISO 3166-2 subdivision flags, as well as the verbosity of flags included, there may exist several outstanding issues with the existing flag icons. A list of countrys that have no recognised subdivisions and hence no flags in iso3166-2 is listed in the file scripts/iso3166-files/noISO3166-2Flags.csv. 
Another outstanding issue is some ISO3166-2 flags not having an existing or easily accessible SVG version of their flag hence some flags are in png/jpg/gif format. Please feel free to do a PR if SVG versions of these flags become available.

Please feel free to raise an Issue in the [Issues](https://github.com/amckenna41/iso3166-2-flag-icons/issues) tab if any incorrect/missing subdivision flags as well as any errors/bugs are found 

Contact
-------

If you have any questions or feedback, please contact amckenna41@qub.ac.uk or visit my [LinkedIn](https://www.linkedin.com/in/adam-mckenna-7a5b22151/):

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/)

License
-----------
Distributed under the MIT License. See `LICENSE` for more details.  

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: https://github.com/lipis/flag-icons <br>
\[4\]: https://github.com/amckenna41/flagle <br>
\[5\]: https://en.wikipedia.org/wiki/ISO_3166-1  <br>


[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
[pandas]: https://pandas.pydata.org/
[tqdm]: https://tqdm.github.io/
[requests]: https://requests.readthedocs.io/
[beautifulsoup4]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
[scour]: https://github.com/scour-project/scour
[pyWikiCommons]: https://github.com/amckenna41/pyWikiCommons
[flag-icons-repo]: https://github.com/lipis/flag-icons
[pycountry]: https://github.com/flyingcircusio/pycountry
[emoji-country-flag]: https://pypi.org/project/emoji-country-flag/
[fuzzywuzzy]: https://pypi.org/project/fuzzywuzzy/

