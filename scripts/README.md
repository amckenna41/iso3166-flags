# Scripts used in iso3166-flags 📜

[![pytest](https://github.com/amckenna41/iso3166-flags/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-flags/actions?query=workflowBuilding%20and%20Testing)
[![Platforms](https://img.shields.io/badge/platforms-linux%2C%20macOS%2C%20Windows-green)](https://pypi.org/project/pySAR/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
<!-- [![codecov](https://codecov.io/gh/amckenna41/iso3166-flags/branch/master/graph/badge.svg?token="")](https://codecov.io/gh/amckenna41/iso3166-flags) -->
<!-- [![npm version](https://badge.fury.io/js/iso3166-flags.svg)](https://badge.fury.io/js/iso3166-flags) -->

Scripts
-------
* [`generate_readme.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/generate_readme.py) - create README files for each ISO 3166-2 subfolder, displaying a plethora of useful data per subdivision including the subdivision codes, names, types, flag previews & link to the flag on the repo. 
* [`generate_css.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/generate_css.py) - create CSS files with respective CSS selectors/classes for the ISO 3166-1, ISO 3166-2 and ISO 3166-3 flag icons, plus SVG sprites, stored in `/css` folder. Flag `url()` paths are written relative to the directory the CSS is served from (`css/` -> `../iso3166-1-flags/...`).
* [`get_flag_metadata`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/get_flag_metadata.py) - export a plethora of useful and relevant metadata for the flag images including name, dimensions, file size, type & quality.
* [`get_missing_flags.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/get_missing_flags.py) - script for exporting a list of subdivisions that have missing or no supported subdivision flags on the repo.
* [`get_git_flag_logs.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/get_git_flag_logs.py) - small script that exports the list of flag additions, modifications and deletions to the repo, exported from the git status command. This is useful to track when a lot of changes have been made to the flags folder.
* [`validate_flags.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/validate_flags.py) - script that checks every flag SVG is safe to inline (no `<script>`, event handlers, `javascript:` or remote references) and every ISO 3166-2 flag is named after a real subdivision code of its country sub-folder. Run with `python3 -m scripts.validate_flags`, exits non-zero on any problem.
* [`update_everything.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/update_everything.py) - script that ensures all the data files and metadata objects used throughout the iso3166-flags project are kept up-to-date when any flags have been added, changed or deleted - the ISO 3166-1/2/3 CSS files (+ minified), the ISO 3166-1 SVG sprite, the per-country ISO 3166-2 READMEs, the ISO 3166-1/2/3 flag metadata CSVs, the repo metadata JSON and the missing subdivision flags list.
* [`convert_images.py`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/convert_images.py) - script for converting all non-jpg/jpeg/png/svg images to the desired formats.
* [`svg_compress.sh`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/svg_compress.sh) - script for compressing folder of image flags in SVG format, reducing the total size of the dataset. Works on both the flat `iso3166-1-flags` layout and the nested `iso3166-2-flags/<country>/` layout, e.g. `bash scripts/svg_compress.sh --input=iso3166-1-flags --output=compressed --filesize=100`.

<!-- * `get_all_subdivision_flags.py` - downloading all ISO3166-2 subdivision flags from the main subdivisions wiki (https://en.wikipedia.org/wiki/Flags_of_country_subdivisions) as well as using country's respective wiki URL's.  -->
<!-- * `generate_json.py` - create JSON files of flag files, their name and ISO code for both ISO3166-1 and ISO3166-2 folders. 
* `iso3166_.py` - list of all ISO3166 country names, alpha2 and alpha3 codes. -->

Requirements
------------

See [`requirements.txt`](https://github.com/amckenna41/iso3166-flags/blob/main/scripts/requirements.txt) for the exact version constraints.

* [python][python] >= 3.10
* [iso3166-2][iso3166_2] == 1.8.4 (pinned - subdivision name/type changes in newer versions alter the generated READMEs)
* [pandas][pandas] >= 2.0.0
* [iso3166][iso3166] >= 2.1.0
* [pillow][pillow] >= 12.3.0 (earlier versions have known vulnerabilities)
* [opencv-python][opencv-python] >= 4.8.0
* [lxml][lxml] >= 5.0.0
* [scour][scour] >= 0.38.2 (for `svg_compress.sh`)

Usage
-----
<i>The below examples should be called from the root dir of the repo.</i>

### Create README files for each ISO 3166-2 subdivision flags in iso3166-2-flags dir:

```bash
python3 scripts/generate_readme.py --flag_input_folder="iso3166-2-flags"

--flag_input_folder: input folder of ISO 3166-2 flag icons to generate README for
--country_subfolder: optional input parameter for a specific country subfolder to create markdown file for
--output_readme_folder: optional output folder to store the generated markdown files, by default they will be stored within the countrys subfolder
```

### Create CSS files for the ISO 3166-1, ISO 3166-2 and ISO 3166-3 flags:

```bash
python3 scripts/generate_css.py --export_iso3166_1_css_filepath="css/iso3166-1.css" --export_iso3166_2_css_filepath="css/iso3166-2.css" --export_iso3166_3_css_filepath="css/iso3166-3.css" --minify

--iso3166_1_country_input_folder: input folder of ISO 3166-1 flags
--iso3166_2_country_input_folder: input folder of ISO 3166-2 flags
--iso3166_3_country_input_folder: input folder of ISO 3166-3 (former country) flags
--export_iso3166_1_css_filepath: export filename for ISO 3166-1 CSS
--export_iso3166_2_css_filepath: export filename for ISO 3166-2 CSS
--export_iso3166_3_css_filepath: export filename for ISO 3166-3 CSS
--iso3166_type: create only the iso3166-1, iso3166-2 or iso3166-3 CSS file, by default all three will be created
--css_dir: directory the CSS will be served from, which flag url() paths are made relative to (default: the directory of each export filepath)
--minify: additionally generate a .min.css minified version of each CSS file
--sprite: generate an SVG sprite file (css/iso3166-1-sprite.svg) for all ISO 3166-1 flags
--export_sprite_filepath: output path for the SVG sprite file (default: css/iso3166-1-sprite.svg)
--iso3166_2_sprite: generate an SVG sprite file for all ISO 3166-2 flags
--iso3166_2_sprite_per_country: generate one smaller SVG sprite file per country instead of a single global sprite (recommended given the ~2,800 flag ISO 3166-2 dataset)
--export_iso3166_2_sprite_filepath: output path for the global ISO 3166-2 SVG sprite file (default: css/iso3166-2-sprite.svg), used unless --iso3166_2_sprite_per_country is set
--export_iso3166_2_sprite_dir: output directory for the per-country ISO 3166-2 SVG sprite files (default: css/iso3166-2-sprites), used when --iso3166_2_sprite_per_country is set
```

### Export flag metadata for ISO 3166-1, ISO 3166-2 or ISO 3166-3 flags:
```bash
python3 scripts/get_flag_metadata.py --flag_folder="iso3166-1-flags" --flag_metadata_output="iso3166_1_flag_metadata.csv"

--flag_folder: file path to folder of flags - iso3166-1-flags and iso3166-3-flags are keyed by a country_code column, iso3166-2-flags by subdivision_code
--flag_metadata_output: output file name for metadata csv
--export_repo_metadata: additionally export the whole-repo metadata object (flag counts, formats, folder sizes, missing flag counts)
--repo_metadata_output: output file name/path for the whole-repo metadata export
--exclude_readme: exclude the country markdown files from the overall file count and metadata calculation (default)
```


### Export list of all ISO 3166-2 subdivisions that have no supported flag in the repo:

```bash
python3 scripts/get_missing_flags.py --flag_icons_dir="iso3166-2-flags" --export_filename="missing_flags"

--flag_icons_dir: input directory of subdivision flags to compare against list of ISO 3166-2 flags
--export_filename: filename for exported list of missing subdivision flags
```


### Export all of the above data objects and matadata files in one script:

```bash
python3 scripts/update_everything.py

--dry-run: preview changes without modifying any files - outputs are written to a temporary directory (cleaned up after) and a summary of what would change is printed
--check: like --dry-run, but also diffs the generated CSS/README/metadata files against what's currently committed and exits non-zero if anything is stale; useful as a CI gate to catch flags being added/changed without regenerating the derived files
```


### Check the flag SVGs are safe and the ISO 3166-2 filenames are valid:

```bash
python3 -m scripts.validate_flags

--flag_dirs: comma-separated list of flag folders whose SVGs are safety checked (default iso3166-1-flags,iso3166-2-flags,iso3166-3-flags)
--iso3166_2_dir: ISO 3166-2 flag folder whose filenames are validated, pass an empty string to skip (default iso3166-2-flags)
```


### Convert all GIF or WEBP images in the flag directory into png

```bash
python3 scripts/convert_images.py 

--flag_folder: input folder of ISO 3166 flag icons to convert to specified format
--archive_folder: optional archive folder that maintains the original unconverted ISO 3166 flag icons
--img_filepath: filepath to individual image to convert. The file will take precedence over a folder of images input
--img_format: file format to convert the images into, accepted formats are png, jpg or jpeg (png by default)
```

### Compress all SVG flag icon files in output folder:

```bash
bash scripts/svg_compress.sh --input="iso3166-2-flags" --output="output" --filesize=50

--input: input folder of flags to compress, either flat (iso3166-1-flags) or nested by country (iso3166-2-flags) - sub-folders are mirrored in the output
--output: output folder to store the compressed SVG files (non-SVG files are copied across unchanged)
--filesize: all SVG files above this threshold (KB) will go through the compression algorithm
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
[scour]: https://pypi.org/project/scour/
[unittest]: https://docs.python.org/3/library/unittest.html

[Back to top](#TOP)