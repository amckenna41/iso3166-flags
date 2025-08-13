<a name="TOP"></a>

# Dataset of all ISO 3166-1 and ISO 3166-2 country and regional flags 🌎

[![pytest](https://github.com/amckenna41/iso3166-flag-icons/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-flag-icons/actions?query=workflowBuilding%20and%20Testing)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-flag-icons)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons/issues)
[![Size](https://img.shields.io/github/repo-size/amckenna41/iso3166-flag-icons)](https://github.com/amckenna41/iso3166-flag-icons)
<!-- [![Commits](https://img.shields.io/github/commit-activity/w/amckenna41/iso3166-flag-icons)](https://github.com/iso3166-flag-icons) -->
<!-- [![npm version](https://badge.fury.io/js/iso3166-flags.svg)](https://badge.fury.io/js/iso3166-flags) -->

> **iso3166-flag-icons** is a bespoke, verbose and comprehensive dataset of all <em>ISO 3166-1</em> & <em>ISO 3166-2</em> country and regional/subdivision codes flag icons in SVG format. The dataset currently has **271** country/territorial flags and **3,213** regional/subdivision flags.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="400" width="700"/>
</p>

<!-- View demo [here](https://amckenna41.github.io/iso3166-flag-icons-website/) ([repo](https://github.com/amckenna41/iso3166-flag-icons-website)). -->

<!-- Quick Start 🏃
------------- -->
## Quick Stats 🏃

| Total Flags |    ISO3166-1 Flags   |    ISO3166-2 Flags    |  SVG  |  PNG  | JPEG / JPG | Other | Total Dataset Size (MB) | ISO3166-1 Dataset Size (MB) | ISO3166-2 Dataset Size (MB) |
|-------------|------------------------|------------------------|-------|-------|------------|-------|-------------------------|------------------------------|------------------------------|
| 3,213       | 271                    | 2,942                  | 2,228 | 908   | 71         | 0     | 474.121                 | 1.956                        | 472.166                      |



Table of Contents
-----------------
  * [Introduction](#introduction)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Updates](#updates)
  * [Directories](#directories)
  * [Issues or Contributing](#issues-or-contributing)
  * [Contact](#contact)
  * [References](#references)
  * [Support](#support)

  <!-- * [License](#license) -->
  <!-- * [Installation](#installation) -->
  <!-- * [Requirements](#requirements) -->


## Introduction
`iso3166-flag-icons` is a **comprehensive**, **verbose** and **bespoke** repository of all ISO 3166-1 and ISO 3166-2 country and regional/subdivsion flag icons, respectively. The flags list is according to the International Organisation for Standards that define codes for the names of countries, dependent territories, special areas of geographical interest, and their principal subdivisions [[1]](#references). 

**Currently the dataset contains <em>271</em> ISO 3166-1 country/territorial flag icons and <em>3,213</em> ISO 3166-2 regional/subdivision flags.** <br> 

The <b>ISO 3166-1</b> flags are those of the names of countries and their subdivisions that can be broken into three sets of country codes:
* *ISO 3166-1 alpha-2* – two-letter country codes which are the most widely used of the three, and used most prominently for the Internet's country code top-level domains (with a few exceptions).
* *ISO 3166-1 alpha-3* – three-letter country codes which allow a better visual association between the codes and the country names than the alpha-2 codes.
* *ISO 3166-1 numeric* – three-digit country codes which are identical to those developed and maintained by the United Nations Statistics Division, with the advantage of script (writing system) independence, and hence useful for people or systems using non-Latin scripts.

The <b>ISO 3166-2</b> icons are those of the names of countries and their subdivisions – *Part 2: Country subdivision code, defines codes for identifying the principal subdivisions (e.g., provinces, states, departments, regions) of all countries coded in ISO 3166-1.* [[2]](#references). <br>

The <b>ISO 3166-3</b> icons are those of countries and their subdivisions – Part 3: Code for formerly used names of countries, defines codes for country names which have been deleted from ISO 3166-1 since its first publication in 1974. This section of the ISO 3166 is not utilised in this repo.

### Motivation
`iso3166-flag-icons` is a part of a larger suite of my **custom-built and bespoke applications** that utilise the ISO 3166 country and subdivision codes. The primary application is [`iso3166-2`][iso3166_2] which is is a structured lightweight custom-built Python package and dataset, and accompanying RESTful API, that can be used to access all of the world's ISO 3166-2 subdivision data. 

One of the attributes in the `iso3166-2` software package is the `flag` attribute - the subdivisions offical flag. When creating this dataset, there was no accurate or widely available dataset of the world's thousands of regional flags, **so I created one!** 

<!-- Alongside the `iso3166-2` software, I also created the [`iso3166-updates`][iso3166_updates] repo. This is a software and accompanying REST API that checks for any updates/changes to the ISO 3166-1 and ISO 3166-2 country codes and subdivision naming conventions, as per the ISO 3166 newsletter (https://www.iso.org/iso-3166-country-codes.html) and Online Browsing Platform (OBP) (https://www.iso.org/obp/ui). Thus it ensures the `iso3166-2` and `iso3166-flag-icons` are kept up-to-date. -->

<!-- ### Motivation

The main motivation behind this project was to integrate additional flag icons into my custom-built web-app <b>Flagle</b> (https://flagle.vercel.app/). This daily worldle-inspired game generates a new flag from around the world each day, consisting of flags of countries, territories and everywhere in between. <br>

After searching around, it was fairly straightforward to find a repo with ISO 3166-1 flags, an example being [here][flag-icons-repo] but there didn't seem to be any single repo/dataset of all ISO 3166-2 subdivision flags, hence I decided to make one from scratch. <br> -->

## Installation
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
The flags can be implemented in-line by referencing the CSS class of the respective flag using the [`ISO 3166-1`](https://github.com/amckenna41/iso3166-flag-icons/css/iso3166-1.css) or [`ISO 3166-2`](https://github.com/amckenna41/iso3166-flag-icons/css/iso3166-1.css) CSS file. For ISO 3166-1 icons add the classes `.fi` and `.fi-xx` (where `xx` is the ISO 3166-1-alpha-2 code of a country) to an empty `<span>` [[5]](#references). To add a squared version flag additionally add the class `fis`. 

For example, adding the normal and squared flags for Andorra, Denmark & Panama:
```html
<span class="fi fi-ad"></span> <span class="fi fi-ad fis"></span>
<span class="fi fi-dk"></span> <span class="fi fi-dk fis"></span>
<span class="fi fi-pa"></span> <span class="fi fi-pa fis"></span>
```

For ISO 3166-2 icons add the classes `.fi` and `.fi-xx-yy` (where `xx` is the ISO 3166-1-alpha-2 code of a country and `yy` is the ISO 3166-2 code, both in lower-case) to an empty `<span>` [[2]](#references). 

For example, adding the Hungarian county of Heves (HU-HE), the South Sudanese state of Eastern Equatoria (SS-EE) & the Taiwanese county of Miaoli (TW-MIA):
```html
<span class="fi fi-hu-he"></span> <span class="fi fi-hu-he fis"></span>
<span class="fi fi-ss-ee"></span> <span class="fi fi-ss-ee fis"></span>
<span class="fi fi-tw-mia"></span> <span class="fi fi-tw-mia fis"></span>
```

Updates
-------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. These changes can happen due for a variety of geopolitical and administrative reasons. Therefore, it's important that this library and its JSON have the most **up-to-date, accurate and reliable data**. To achieve this, the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo was created!

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo is another open-source software package and accompanying RESTful API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. A script is called periodically to check for any updates/changes to the subdivisions, which are communicated via the ISO's Online Browsing Platform [[4]](#references), and will then be manually incorporated into this repo. Please visit the repository home page for more info about the purpose and process of the software and API - [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates).

The list of ISO 3166 updates was last updated on <strong>November 2024</strong> (the last published ISO subdivision change). A log of the latest ISO 3166 updates can be seen in the [UPDATES.md][updates_md] file.

Directories 
-----------
* [`/iso3166-1-icons`](https://github.com/amckenna41/iso3166-flag-icons/tree/main/iso3166-1-icons) - flags of all country/territories according to the ISO 3166-1 standard.
* [`/iso3166-2-icons`](https://github.com/amckenna41/iso3166-flag-icons/tree/main/iso3166-2-icons)  - flags of all regions/subdivisions within countries/territories according to the ISO 3166-2 standard.
* [`/css`](https://github.com/amckenna41/iso3166-flag-icons/tree/main/css) - css scripts for integrating the flags into front-end projects.
* [`/scripts`](https://github.com/amckenna41/iso3166-flag-icons/tree/main/scripts) - a series of Python and bash scripts created for generating the CSS and README files for each country folder, as well as to export various metdata for the datasets.
* [`/tests`](https://github.com/amckenna41/iso3166-flag-icons/tree/main/tests) - unit tests for scripts and flags.

<!-- * `iso3166-1.json` - json containing all ISO 3166-1 country names, 2 letter codes and relative path to flag icon in repo.
* `iso3166-2.json` - json containing all ISO 3166-2 country names, 2 letter codes, all subdivision codes and common names as well as all info pulled per country via the restcountries api (https://restcountries.com/). 
* `iso3166-2-min.json` - minimised json containing all ISO 3166-2 country names, 2 letter codes and all subdivision codes and common names. -->
<!-- * `index.html` - front-end demo for iso3166-flag-icons repo. -->
<!-- * `/downloads` - directory of zipped iso3166-1 and iso3166-2 flag icons files. -->
<!-- * `/scripts` - various Python and bash scripts created for downloading and compressing all the required flag SVG files for both the ISO 3166-1 and ISO 3166-2 icons, as well as scripts for creating the json, CSS and readme files. -->

## Other ISO 3166 repositories
Below are some of my other **custom-built** repositories that relate to the ISO 3166 standard! ⚡
* [iso3166-2](): a lightweight custom-built bespoke Python package, dataset, and accompanying API, that can be used to access all of the world's ISO 3166-2 subdivision data. A plethora of data attributes are available per country and subdivision including: name, local name, code, parent code, type, lat/longitude and flag. Currently, the package and API supports data from 250 countries/territories, according to the ISO 3166-1 standard and >5000 subdivisions, according to the ISO 3166-2 standard.
* [iso3166-2-api](https://github.com/amckenna41/iso3166-2-api): frontend RESTful API for iso3166-2.
* [iso3166-updates](https://github.com/amckenna41/iso3166-update): software and accompanying RESTful API that checks for any updates/changes to the ISO 3166-1 and ISO 3166-2 country codes and subdivision naming conventions, as per the ISO 3166 newsletter (https://www.iso.org/iso-3166-country-codes.html) and Online Browsing Platform (OBP) (https://www.iso.org/obp/ui).
* [iso3166-updates-api](https://github.com/amckenna41/iso3166-updates-api): frontend RESTful API for iso3166-updates.
<!-- * [iso3166-2-export](https://github.com/amckenna41/iso3166-2-export): scripts for full ISO 3166-2 subdivision data export. -->

## Issues or Contributing
Any issues, bugs or enhancements can be raised via the [Issues][issues] tab in the repository. If you would like to contribute any functional/feature changes to the project, please make a Pull Request.

<!-- Also, due to the large amount of data and attributes in the dataset, please raise an Issue if you spot any missing or erroneous data. When raising this Issue please include the current subdivision object attribute values as well as the corrected/new version of them in an easy-to-read format.  -->

## Contact
If you have any questions, comments or suggestions, please contact amckenna41@qub.ac.uk or raise an issue in the [Issues][issues] tab.  

<!-- License
-----------
Distributed under the MIT License. See `LICENSE` for more details.   -->

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166 <br>
\[2\]: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 <br>
\[4\]: https://www.iso.org/obp/ui/#

## Support
[<img src="https://img.shields.io/github/stars/amckenna41/iso3166-flag-icons?color=green&label=star%20it%20on%20GitHub" width="132" height="20" alt="Star it on GitHub">](https://github.com/amckenna41/iso3166-flag-icons)

<a href="https://www.buymeacoffee.com/amckenna41" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

[Back to top](#TOP)

[python]: https://www.python.org/downloads/release/python-360/
[pandas]: https://pandas.pydata.org/
[tqdm]: https://tqdm.github.io/
[requests]: https://requests.readthedocs.io/
[beautifulsoup4]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
[scour]: https://github.com/scour-project/scour
[pyWikiCommons]: https://github.com/amckenna41/pyWikiCommons
[flag-icons-repo]: https://github.com/lipis/flag-icons
[emoji-country-flag]: https://pypi.org/project/emoji-country-flag/
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[fuzzywuzzy]: https://pypi.org/project/fuzzywuzzy/
[iso3166_updates]: https://github.com/amckenna41/iso3166-updates
[Issues]: https://github.com/amckenna41/iso3166-flag-icons/issues
[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md