# Test scripts for testing the flags and various utility scripts in iso3166-flags 🧪

* `test_iso3166_1_flags.py` - testing the ISO 3166-1 flag directory.
* `test_iso3166_2_flags.py` - testing the ISO 3166-2 flag directory.
* `test_flag_metadata.py` - testing the `get_flag_metadata` script, that calculates a plethora of metadata for each of the ISO 3166-1 and ISO 3166-2 flags.
* `test_generate_css.py` - testing the `generate_css` script, that exports the ISO 3166-1 and ISO 3166-2 CSS files.
* `test_generate_readme.py` - testing the `generate_readme` script, that exports the ISO 3166-2 markdown files per subdivision sub-folder.
* `test_get_missing_flags.py` - testing the `get_missing_flags` script, that exports list of all subdivisions that don't have an associated flag on the repo.