# flag-icons
A comprehensive library of ISO3166-1/2 country/subdivision codes and their corresponding flag icons.

[![PythonV](https://img.shields.io/pypi/pyversions/pySAR?logo=2)](https://pypi.org/project/pySAR/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/DCBLSTM_PSP)](https://github.com/amckenna41/iso3166-2-flag-icons/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/DCBLSTM_PSP)](https://github.com/amckenna41/iso3166-2-flag-icons)
[![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-2-flag-icons)](https://github.com/iso3166-2-flag-icons)

Table of Contents
-----------------

  * [Introduction](#introduction)
  * [Purpose](#approach)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Directory Folders](#directory-folders)
  * [Open Issues](#Issues)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------

Purpose
-------

Requirements
------------

* [Python][python] >= 3.6
* [numpy][numpy] >= 1.16.0

requests
tqdm
beautifulsoup4
iso3166
SVGCompress
scour 

Directory folders
-----------------

* `/iso3166-1-icons` - flags of all country/territories/subdivisions according to the ISO3166-1 standard [].
* `/iso3166-2-icons` - flags of all subdivisions within countries/territories according to the ISO3166-2 standard [].
* `/scripts` - various Python and bash scripts created for downloading and compressing all the required flag SVG files for
both the ISO3166-1 and ISO3166-2 icons. 


Issues
------
Due to the nature of the methodology for getting the ISO3166-2 subdivision flags (via web scraping) there may exist several outstanding issues with the dataset of icons such as corrupt files, low quality files, large files etc; although, I am in the process of going through each country and file to correct this. Another issue may be incorrect or missing flags for certain countries/territories, although I take no liability for these as all flags were taken from the "Flags of country subdivisions" wiki page [3]. Although please feel free to raise an Issue in the [Issues](https://github.com/amckenna41/iso3166-2-flag-icons/issues) tab for any such cases and I will try to rectify it.

Any other issues, errors or bugs can be raised via the [Issues](https://github.com/amckenna41/iso3166-2-flag-icons/issues) tab in the repository.

Contact
-------

If you have any questions or feedback, please contact amckenna41@qub.ac.uk or visit my [LinkedIn](https://www.linkedin.com/in/adam-mckenna-7a5b22151/):

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adam-mckenna-7a5b22151/)


References
----------
\[1\]:
\[2\]:
\[3\]: https://en.wikipedia.org/wiki/ISO_3166
https://en.wikipedia.org/wiki/ISO_3166-2

[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
