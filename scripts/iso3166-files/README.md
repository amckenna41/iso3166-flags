# ISO3166-2-flag-icons external files required for scripts

* `iso3166-2_urls.csv` - CSV file containing all the wiki URLs for all applicable ISO3166-2 entities. The wiki URL for each country will be used for web scraping using BS4 to download all the required subdivision flags in the getISO3166-2Flags.py script.
* `noISO3166-2Flags.csv` - csv file with list of all ISO3166-2 countries/territories that either do not have any ISO3166-2 subdivisions OR their listed subdivisions do not have any applicable or available flags (https://en.wikipedia.org/wiki/ISO_3166-2).

