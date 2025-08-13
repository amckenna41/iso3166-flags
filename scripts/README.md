# Scripts used in iso3166-flag-icons 📜

[![pytest](https://github.com/amckenna41/iso3166-flag-icons/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-flag-icons/actions?query=workflowBuilding%20and%20Testing)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/pySAR/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
<!-- [![codecov](https://codecov.io/gh/amckenna41/iso3166-flag-icons/branch/master/graph/badge.svg?token="")](https://codecov.io/gh/amckenna41/iso3166-flag-icons) -->
<!-- [![npm version](https://badge.fury.io/js/iso3166-flags.svg)](https://badge.fury.io/js/iso3166-flags) -->

Scripts
-------
* [`generate_readme.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/generate_readme.py) - create README files for each ISO 3166-2 subfolder, displaying a plethora of useful data per subdivision including the subdivision codes, names, types, flag previews & link to the flag on the repo. 
* [`generate_css.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/generate_css.py) - create CSS files with respective CSS selectors/classes for both ISO 3166-1 and ISO 3166-2 flag icons, stored in `/css` folder.
* [`get_flag_metadata`](https://github.com/amckenna41/iso3166-flag-icons/scripts/get_flag_metadata.py) - export a plethora of useful and relevant metadata for the flag images including name, dimensions, file size, type & quality.
* [`get_missing_flags.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/get_missing_flags.py) - script for exporting a list of subdivisions that have missing or no supported subdivision flags on the repo.
* [`get_git_flag_logs.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/get_git_flag_logs.py) - small script that exports the list of flag additions, modifications and deletions to the repo, exported from the git status command. This is useful to track when a lot of changes have been made to the flags folder.
* [`update_everything.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/update_everything.py) - script that ensures all the data files and metadata objects used throughout the iso3166-flag-icons project are kept up-to-date when any flags have been added, changed or deleted.
* [`convert_images.py`](https://github.com/amckenna41/iso3166-flag-icons/scripts/convert_images.py) - script for converting all non-jpg/jpeg/png/svg images to the desired formats.
* [`svg_compress.sh`](https://github.com/amckenna41/iso3166-flag-icons/scripts/svg_compress.sh) - script for compressing folder of image flags in SVG format, reducing the total size of the dataset.

<!-- * `get_all_subdivision_flags.py` - downloading all ISO3166-2 subdivision flags from the main subdivisions wiki (https://en.wikipedia.org/wiki/Flags_of_country_subdivisions) as well as using country's respective wiki URL's.  -->
<!-- * `generate_json.py` - create JSON files of flag files, their name and ISO code for both ISO3166-1 and ISO3166-2 folders. 
* `iso3166_.py` - list of all ISO3166 country names, alpha2 and alpha3 codes. -->

Requirements
------------

* [python][python] >= 3.9
* [iso3166-2][iso3166_2] >= 1.7.2
* [pandas][pandas] >= 1.4.3
* [iso3166][iso3166] >= 2.1.1
* [pillow][pillow] >= 11.3.0
* [opencv-python][opencv-python] >= 4.12.0.88
* [lxml][lxml] >= 6.0.0

Usage
-----
<i>The below examples should be called from the root dir of the repo.</i>

### Create README files for each ISO 3166-2 subdivision flags in iso3166-2-icons dir:

```bash
python3 scripts/generate_readme.py --flag_input_folder="../iso3166-2-icons"

--flag_input_folder: input folder of ISO 3166-2 flag icons to generate README for
--country_subfolder: optional input parameter for a specific country subfolder to create markdown file for
--output_readme_folder: optional output folder to store the generated markdown files, by default they will be stored within the countrys subfolder
```

### Create CSS files for both ISO 3166-1 and ISO 3166-2 flags:

```bash
python3 scripts/generate_css.py --iso3166_1_country_input_folder="../iso3166-1-icons" --iso3166_2_country_input_folder="../iso3166-2-icons" --export_iso3166_1_css_filepath="iso3166-1-icons.css"  --export_iso3166_1_css_filepath="iso3166-2-icons.css"

--iso3166_1_country_input_folder: input folder of ISO 3166-1 flags
--iso3166_2_country_input_folder: input folder of ISO 3166-2 flags
--export_iso3166_1_css_filepath: export filename for ISO 3166-1 CSS
--export_iso3166_2_css_filepath: export filename for ISO 3166-2 CSS
--iso3166_type: create ISO3166-1 or ISO3166-2 CSS file, by default both will be created
```

### Export flag metadata for ISO 3166-1 and ISO 3166-2 flags:
```bash
python3 scripts/export_flag_metadata.py --flag_folder="../iso3166-1-icons" --flag_metadata_output="subdivision_flag_metadata.csv"

--flag_folder: file path to folder of nested subdivision flags
--flag_metadata_output: output file name for metadata csv
```


### Export list of all ISO 3166-2 subdivisions that have no supported flag in the repo:

```bash
python3 scripts/get_missing_flags.py --flag_icons_dir="iso3166-2-icons" --export_filename="missing_flags"

--flag_icons_dir: input directory of subdivision flags to compare against list of ISO 3166-2 flags
--export_filename: filename for exported list of missing subdivision flags
```


### Export all of the above data objects and matadata files in one script:

```bash
python3 scripts/update_everything.py
```


### Convert all GIF or WEBP images in the flag directory into png

```bash
python3 scripts/convert_images.py 

--flag_folder: input folder of ISO 3166 flag icons to convert to specified format
--archvive_folder: optional archive folder that maintains the original unconverted ISO 3166 flag icons
--img_file_path: filepath to individual image to convert. The file will take precedence over a folder of images input
--img_format: file format to convert the images into, accepted formats are png, jpg or jpeg (png by default)
```

### Compress all SVG flag icon files in output folder:

```bash
./scripts/svgCompress.sh --input="../iso3166-2-icons/" --output="../output/" --filesize=50

--input: input folder of SVG files to compress
--output: output folder to store compressed SVG files
--filesize_threshold: all SVG files above this threshold will go through the compression algorithm. 
```

<!-- 3511 seconds total-->
[python]: https://www.python.org/downloads/release/python-360/
[pandas]: https://pandas.pydata.org/
[flag-icons-repo]: https://github.com/lipis/flag-icons
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[iso3166]: https://github.com/deactivated/python-iso3166
[pillow]: https://pypi.org/project/pillow/
[opencv-python]: https://pypi.org/project/opencv-python/
[lxml]: https://pypi.org/project/lxml/
[unittest]: https://docs.python.org/3/library/unittest.html

[Back to top](#TOP)