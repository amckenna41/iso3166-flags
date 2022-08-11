# Scripts for downloading all ISO3166-2 country subdivision flags

* `getAllSubdivisionFlags.py` - downloading all ISO3166-2 subdivision flags from the main subdivisions wiki (https://en.wikipedia.org/wiki/Flags_of_country_subdivisions).
* `getISO3166-2Flags.py` - download remaining ISO3166-2 subdivision flags from each countrys respecitve wiki.
* `generateReadMe.py` - create README file for each ISO3166-2 subfolder, listing all the subdivisions per country.
* `generateCSS.py` - create CSS files with respective CSS selectors/classes for both ISO3166-2 and ISO3166-2 flag icons.
* `generateJSON.py` -
* `svgCompress.sh` - script for compressing folder of SVG files.

Usage
-----

## Get all flags from subdivions wiki (https://en.wikipedia.org/wiki/Flags_of_country_subdivisions)

```bash
python3 getAllSubdivisionFlags.py --output="../countries"
```

## Get remainder of flags according to iso3166-files/iso3166-2_urls.csv

```bash
python3 getISO3166-2Flags.py --output="../countries" --url_wiki_csv="iso3166-2_urls.csv"
```

## Get all flags using both scripts

```bash
python3 getAllSubdivisionFlags.py --output="../countries" && python3 getISO3166-2Flags.py --output="../countries" --url_wiki_csv="iso3166-2_urls.csv"
```

## Compress all SVG flag icon files in output folder

```bash
./svgCompress.sh --input="../countries/" --output="../output/" --filesize_threshold=50

--input: input folder of SVG files to compress
--output: output folder to store compressed SVG files
--filesize_threshold: all SVG files above this threshold will go through the compression algorithm. 

```

## Create CSS files for both ISO3166-1 and ISO3166-2 icons

```bash
python3 generateCSS.py --countryFolder="../iso3166-1-icons" --cssFileName="iso3166-1-icons.css" --iso3166Type="iso3166-1"
```

## Create ISO3166-1 or ISO3166-2 JSON files containing all flag and subdivision info per country/jurisdiction

```python
```

178 seconds for getAll
3333 seconds for getISO...