# Test scripts for testing the flags and various utility scripts in iso3166-flags 🧪

## Flag Dataset Tests

* `test_iso3166_1_flags.py` - testing the ISO 3166-1 flag directory: completeness against the official ISO 3166-1 codes, file formats/sizes and SVG validity. Non-official flags, including the 13 reserved-code flags (`ac`, `cp`, `cq`, `dg`, `ea`, `eu`, `ez`, `fx`, `ic`, `su`, `ta`, `uk`, `un`), are listed in `EXCEPTION_FLAGS`.
* `test_iso3166_2_flags.py` - testing the ISO 3166-2 flag directory. `MAX_OVERSIZED_FILES` caps the number of flags over 500KB and should be lowered whenever flags are compressed (the test tells you the new value).
* `test_iso3166_3_flags.py` - testing the ISO 3166-3 (former country) flag directory.

## Script Tests

* `test_flag_metadata.py` - testing the `get_flag_metadata` script, that calculates a plethora of metadata for each of the ISO 3166-1, ISO 3166-2 and ISO 3166-3 flags, including malformed SVG handling.
* `test_generate_css.py` - testing the `generate_css` script, that exports the ISO 3166-1, ISO 3166-2 and ISO 3166-3 CSS files and the SVG sprites - including that every flag `url()` resolves relative to the stylesheet, the `.fi::before` rule, and unique/namespaced sprite ids.
* `test_generate_readme.py` - testing the `generate_readme` script, that exports the ISO 3166-2 markdown files per subdivision sub-folder.
* `test_get_missing_flags.py` - testing the `get_missing_flags` script, that exports list of all subdivisions that don't have an associated flag on the repo.
* `test_get_git_flag_logs.py` - testing the `get_git_flag_logs` script, that exports the list of flag additions, modifications and deletions from the git status command.
* `test_convert_images.py` - testing the `convert_images` script, that converts the flag images into different format.
* `test_validate_flags.py` - testing the `validate_flags` script, that rejects unsafe SVG content (scripts, event handlers, `javascript:` and remote references), SVG references to missing elements, raster flags whose content doesn't match their extension, and misnamed/misplaced ISO 3166-2 flags.
* `test_svg_compress.py` - testing the `svg_compress.sh` script on both flat and nested flag folders (skipped if `scour` isn't installed).

`tests/test_flags/` is a small fixture of subdivision flags used by the script tests.

The committed CSS, sprite, README and metadata files are checked against the flag folders separately in CI via `python -m scripts.update_everything --check`, and every flag in the repo is checked via `python -m scripts.validate_flags`.

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_flag_metadata.py

# Run a single test
python -m pytest tests/test_generate_css.py::Generate_CSS_Tests::test_background_image_urls

# Run with verbose output
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=scripts --cov-report=html
```

## Test Dependencies

See `requirements.txt` for required packages. Install with:
```bash
pip install -r tests/requirements.txt
```