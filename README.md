# iso3166-flag-icons

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons)
[![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-flag-icons)](https://github.com/iso3166-flag-icons)

> ** In development - ISO3166-2 flags completed from AD-DK **

> A comprehensive library of ISO3166-1 & ISO3166-2 country/subdivision codes and their corresponding flag icons in SVG format. View demo [here]().

Table of Contents
-----------------

  * [Introduction](#introduction)
  * [Motivation](#motivation)
  * [Usage](#usage)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Methodology][#methodology]
  * [Directory Folders](#directory-folders)
  * [Open Issues](#Issues)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------
ISO3166-flag-icons is a comprehensive repository of all ISO3166-1 and ISO3166-2 flag icons according to the International Organisation for Standard that defines codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). <br>

The <b>ISO3166-1</b> icons are those of the names of countries and their subdivisions that can be broken into three sets of country codes:
* ISO 3166-1 alpha-2 – two-letter country codes which are the most widely used of the three, and used most prominently for the Internet's country code top-level domains (with a few exceptions).
* ISO 3166-1 alpha-3 – three-letter country codes which allow a better visual association between the codes and the country names than the alpha-2 codes.
* ISO 3166-1 numeric – three-digit country codes which are identical to those developed and maintained by the United Nations Statistics Division, with the advantage of script (writing system) independence, and hence useful for people or systems using non-Latin scripts.

The <b>ISO3166-2</b> icons are those of the names of countries and their subdivisions – Part 2: Country subdivision code, defines codes for the names of the principal subdivisions (e.g., provinces, states, departments, regions) of all countries coded in ISO 3166-1 [[2]](#references). <br>

The <b>ISO 3166-3</b> icons are those of countries and their subdivisions – Part 3: Code for formerly used names of countries, defines codes for country names which have been deleted from ISO 3166-1 since its first publication in 1974.


Motivation
----------
The main motivation behind this project was to integrate additional flag icons into my custom-built web-app <b>Flagle</b> (https://flagle.vercel.app/). This daily worldle-inspired game generates a new flag from around the world each day, consisting of flags of countries, territories and everywhere in between. <br>

After searching around, it was fairly straightforward to find a repo with ISO3166-1 flags, an example being [here][flag-icons-repo] but there didn't seem to be any single repo/dataset of all ISO3166-2 subdivision flags, hence I decided to make one myself. <br>

Installation
------------
- A zipped folder of all ISO3166-1 OR ISO3166-2 flag icons are available to download in the /downloads folder of the repo.

The whole project can be cloned from git:
```
git clone https://github.com/amckenna41/iso3166-flag-icons.git
```

The ISO3166-1 and ISO3166-2 are also split into branches and be downloaded seperately, so the ISO3166-1 branch can be downloaded using:
```
git clone -b iso3166-1-icons https://github.com/amckenna41/iso3166-flag-icons.git 
```

Install via npm or yarn (<b><i>not implemented yet</i></b>):
```
npm install --dev iso3166-flag-icons

yarn add --dev iso3166-flag-icons
```

Usage
-----

The flags can be implemented in-line by referencing the CSS class of the respective flag using the ISO3166-1 or ISO3166-2 CSS file. For ISO3166-1 icons add the classes `.fi` and `.fi-xx` (where `xx` is the ISO 3166-1-alpha-2 code [[2]](#references) of a country) to an empty `<span>`. To add a squared version flag then additionally add the class `fis`. Example: 

```html
<span class="fi fi-ad"></span> <span class="fi fi-ad fis"></span>
```

For ISO3166-2 icons add the classes `.fi` and `.fi-xx-yy` (where `xx` is the ISO 3166-1-alpha-2 code [[2]](#references) of a country and `yy` is the ISO 3166-2 code) to an empty `<span>`. 

```html
<span class="fi fi-ad-02"></span> <span class="fi fi-ad-02 fis"></span>
```
Methodology
-----------

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


Directory folders
-----------------

* `/iso3166-1-icons` - flags of all country/territories/subdivisions according to the ISO3166-1 standard [].
* `/iso3166-2-icons` - flags of all subdivisions within countries/territories according to the ISO3166-2 standard [].
* `/scripts` - various Python and bash scripts created for downloading and compressing all the required flag SVG files for
both the ISO3166-1 and ISO3166-2 icons. 
* `/downloads` - directory of zipped iso3166-1 and iso3166-2 flag icons files.
* `/css` - css scripts for integrating the flags into front-end projects.
* `/images` - directory for any images used in repo.

Issues
------
Due to the nature of the methodology for getting the ISO3166-2 subdivision flags (via web scraping) there may exist several outstanding issues with the dataset of icons including incorrect or missing flags for certain countries/territories. Please feel free to raise an Issue in the [Issues](https://github.com/amckenna41/iso3166-2-flag-icons/issues) tab for any such cases and I will try to rectify it.

Any other issues, errors or bugs can be raised via the [Issues](https://github.com/amckenna41/iso3166-2-flag-icons/issues) tab in the repository.

Contact
-------

If you have any questions or feedback, please contact amckenna41@qub.ac.uk or visit my [LinkedIn](https://www.linkedin.com/in/adam-mckenna-7a5b22151/):

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/)


References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: https://github.com/lipis/flag-icons <br>
\[4\]: https://github.com/amckenna41/flagle <br>

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


<!-- **all country folders manually checked, removing any unneeded imgs and renaming etc. -->


<!-- Add unit tests - check nunber of imgs downloaded = total on subdivisios page, hardcode subdivisions. -->

<!-- Mention that flags are from wikimedia commons and are under creatvie commons license -->