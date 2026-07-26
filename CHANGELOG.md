# Changelog

All notable changes to the **iso3166-flags** project are documented in this file. This project tracks changes to flag assets, metadata structures, and schema updates following ISO 3166-1 and ISO 3166-2 standards.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Latest]

### Added
- `create_iso3166_2_svg_sprite()` in `generate_css.py` for generating SVG sprite file(s) for the ISO 3166-2 subdivision flags, with a `per_country` option to generate one smaller sprite per country (recommended given the ~2,800 flag, 339MB dataset) instead of a single global sprite, plus new `-iso3166_2_sprite`/`-iso3166_2_sprite_per_country` CLI flags
- `--check` flag to `update_everything.py` that runs the same generation as `--dry-run` and diffs the output against the committed CSS/README/metadata files, exiting non-zero if anything is stale
- "Check generated CSS/README/metadata files are up to date" CI step in `build_test.yml` using `update_everything.py --check` as a staleness gate
- `tests/test_get_git_flag_logs.py` test module covering `get_git_flag_logs.py`, including a regression test asserting the parsed git status is forwarded through to the commit-timestamp lookup
- `test_create_iso3166_2_svg_sprite_global`/`test_create_iso3166_2_svg_sprite_per_country` in `tests/test_generate_css.py` covering the new ISO 3166-2 sprite generation
- `test_create_markdown_str_missing_notes_row` in `tests/test_generate_readme.py`, a regression test asserting `create_markdown_str` no longer crashes for a country with zero matching rows in the notes CSV
- "SVG Sprites" usage section in `css/README.md` documenting both the ISO 3166-1 and new ISO 3166-2 sprite generation and `<use>` consumption
- `--iso3166_2_sprite`/`--iso3166_2_sprite_per_country`/`--dry-run`/`--check` flags documented in `scripts/README.md` and `iso3166-flags-metadata/README.md`
- `iso3166-3-flags/` directory containing 24 SVG flag icons for former countries and territories withdrawn from ISO 3166-1, identified by their ISO 3166-3 alpha-4 codes (e.g. `SUHH.svg` for the Soviet Union, `YUCS.svg` for Yugoslavia, `DDDE.svg` for East Germany)
- `iso3166-3-flags/README.MD` documenting the purpose of the folder, the ISO 3166-3 standard, the alpha-4 code naming convention, a full table of all 24 entries with their successor states and active periods, and usage examples
- `tests/test_iso3166_3_flags.py` test module with 10 tests covering flag count, file extensions, alpha-4 naming format, validity against the known ISO 3166-3 code set, duplicate detection, SVG integrity, image dimensions, file size limits, path complexity, and broken image detection
- `test_iso3166_2_file_size_limits` in `tests/test_iso3166_2_flags.py`, the ISO 3166-2 counterpart to the ISO 3166-1 file size cap that the subdivision suite was missing entirely. It enforces a 7,500KB hard per-file ceiling plus a ratchet on the number of flags above the 500KB target (`MAX_OVERSIZED_FILES`, currently 143), so no new oversized flag can be added and the ceiling must be lowered as existing rasters are optimised
- `parse_porcelain_status()` in `get_git_flag_logs.py` for parsing machine-readable `git status` output, covered by `test_parse_porcelain_status` (staged, unstaged, deleted, untracked, renamed, ignored/unmerged entries and paths containing spaces) and `test_export_git_flag_logs_deleted_file`
- `--export_repo_metadata`/`--repo_metadata_output` CLI flags for `get_flag_metadata.py`
- `check_upstream_flags.yml` GitHub Actions workflow that runs quarterly, detects new releases of [lipis/flag-icons](https://github.com/lipis/flag-icons), syncs `iso3166-1-flags/` with the upstream `flags/4x3/` directory, and automatically opens a pull request summarising added, updated, and removed flags
- --dry-run flag to `update_everything.py` for previewing changes without modifications
- Edge case tests for invalid/empty subdivisions in test suite
- Performance tests for CSS generation with 3,000+ flags
- Integration tests to verify script consistency across multiple runs
- Enhanced .gitignore with documentation about generated files
- Data validation to ensure CSV and iso3166-2 package consistency

### Changed
- Fixed metadata JSON average flag size calculation (was showing KB instead of bytes)
- Improved error handling and logging in Python scripts
- Enhanced documentation for local development setup
- `get_git_flag_logs.py` now parses `git status --porcelain=v1 -z` via a new `parse_porcelain_status()` function instead of scraping the human-readable `git status` output, which was localised, silently dropped all staged changes and broke on paths containing spaces
- `convert_images.py` now walks the flag folder recursively via a single `convert_one_img()` helper rather than three near-identical hand-rolled loops limited to two directory levels
- `generate_readme.py` reads the notes CSV lazily via `get_notes_df()` on first use instead of at module import, so importing the module no longer depends on the current working directory or on the notes file existing
- Bumped `package.json` version from `1.0.2` to `2.4.1` to match the repository/release version
- The `-o/--output` argument of `update_everything.py` and the corresponding `output_folder` parameter have been removed; they were parsed and documented but never used
- The `-img_file_path` argument of `convert_images.py` is now `-img_filepath`, matching the function parameter it feeds
- `-flag_folder`/`-flag_input_folder` defaults in `convert_images.py` and `generate_readme.py` now point at the real `iso3166-2-flags` directory instead of the non-existent `iso3166-2-flags-edit-this-one`

### Security
- `tar.extractall()` in `check_upstream_flags.yml` now extracts with the `filter="data"` member filter (with a manual absolute-path/`..`-traversal/special-file guard as a fallback for interpreters predating the argument). The workflow downloads an external tarball in a runner holding `contents: write` and `pull-requests: write`, so an unfiltered extraction allowed a malicious or compromised upstream release to write outside the extraction directory
- Corrected the Bandit invocation in `build_test.yml` from `--level`/`--confidence` to `--severity-level`/`--confidence-level`. The invalid flags made Bandit exit with a usage error that `|| true` and `continue-on-error` swallowed, so the security job had been reporting success without scanning anything

### Fixed
- `export_git_flag_logs()` raising `OSError: Filepath not found` and aborting the whole export whenever a flag had been deleted — `extract_file_metadata()` required the path to exist on disk, which deleted files by definition do not
- `convert_images.py` archiving or deleting the original image even when the conversion had failed, losing the source file with no converted replacement written; originals are now only archived/deleted after `convert_one_img()` reports success. This also fixes a `FileNotFoundError` when `archive_folder` and `delete_original` were both set, where the file was moved and then removed from its old path
- `convert_img(**vars(args))` raising `TypeError: unexpected keyword argument 'img_file_path'`, and `create_readme(**vars(args))` raising `TypeError: unexpected keyword argument 'exclude_readme'`, which made both scripts unusable from the command line
- Subdivision names containing commas being written to `missing_subdivision_flags.csv` with doubly-escaped quotes (`"""Bournemouth, Christchurch and Poole"""`) because they were manually quoted before being passed to the CSV writer, which quotes them itself
- `get_flag_metadata.py`'s `__main__` block parsing its arguments and then ignoring all of them, calling only `filter_by_size()` while the real export calls sat commented out; it now exports the per-flag metadata and, with the new `--export_repo_metadata` flag, the whole-repo metadata object
- `filter_by_size()` only descending into sub-directories, so it silently produced an empty result for the flat `iso3166-1-flags` layout; it now walks the folder recursively and raises `OSError` for a missing directory
- `export_flag_metadata()` deciding its first CSV column by exact string comparison against `"iso3166-1-flags"`, so `./iso3166-1-flags`, a trailing slash or an absolute path silently mislabelled the column as `subdivision_code`
- `parse_svg_dimension()` catching `IOError`, which it can never raise, instead of the `ValueError` that malformed numeric dimensions such as `width="1.2.3"` actually produce
- `ZeroDivisionError` in `export_repo_metadata()` when both flag directories are empty
- Weekday abbreviations in `get_git_flag_logs.py` timestamps rendering as "Mons"/"Weds"/"Thus" from `strftime('%a') + 's'`; the duplicated formatting logic is now shared via a single `format_timestamp()` function
- `tests/test_get_git_flag_logs.py` creating `tests/test_output_dir` in `setUp` with no `tearDown` to remove it, leaving the directory behind after every run
- Incorrect return type annotations on `calculate_dimension()`, `create_markdown_str()` and `export_missing_flags()`
- `scripts/README.md` documenting a non-existent `scripts/export_flag_metadata.py`, the removed `-o/--output` flag and the old `--img_file_path` argument name
- Bug in `get_flag_metadata.py` where average_flag_size was calculated in bytes instead of KB
- Inconsistency between missing subdivisions count in CSV (2,203) and JSON metadata (2,204)
- Hardcoded ISO 3166-1/3166-2 flag totals in `tests/test_iso3166_1_flags.py` and `tests/test_flag_metadata.py` that broke whenever flags were added; totals are now derived from the `iso3166`/`iso3166_2` packages instead of fixed numbers, and `test_export_repo_metadata` no longer compares against a frozen snapshot dict
- Invalid `except OSError(...)` exception filter in `get_flag_metadata.py` that raised a `TypeError` instead of falling back to a 0-byte file size
- `create_iso3166_1_css()` not excluding `README.md`/`.DS_Store` the way `create_iso3166_2_css()` already did, which could generate a bogus CSS selector for non-flag files
- Fragile numpy truth-testing in `generate_readme.py`'s notes lookup that raised `ValueError` for countries with zero or multiple matching notes rows
- Malformed `iso3166_flags_metadata/iso3166_flag_notes.csv` (ragged rows with a stray trailing comma on some lines) that caused `pandas.read_csv` to silently misalign the `countryCode`/`notes` columns, and removed the fragile `reset_index()`/`assign()` workaround in `generate_readme.py` that depended on that misalignment
- `get_git_timestamp()` never receiving its `status` argument in `get_git_flag_logs.py`, so the "not-committed" fallback could never trigger; also removed dead unused `modified`/`deleted`/`added` lists
- `export_repo_metadata()` undercounting the `other` file-format bucket (breaking the `total == svg+png+jpg/jpeg+other` invariant) when `exclude_readme=False`
- `update_everything.py --dry-run` reading ISO 3166-2 flags from an empty temp directory instead of the real one, silently producing an empty `iso3166-2.css` and no README preview; per-country READMEs are now correctly previewed via `output_readme_folder` without touching real files, and `missing_subdivision_flags.csv` is also redirected to the temp dir during dry-run/check
- Re-enabled a previously-disabled assertion in `test_generate_readme.py::test_create_markdown_str` for the Mauritius (MU) notes section, which had been commented out; updated its expected subdivision type counts (`District (9), Dependency (3)`) to match the current `iso3166-2` package data
- `iso3166-flags-metadata/README.md` documenting the dry-run flag as `--dry_run` instead of the actual `--dry-run`

---

## [Previous Releases]

### Initial Release + Historical Changes

The project maintains a comprehensive history of flag updates and schema changes. Historical changelog entries include:

#### Flag Changes
- Changed FR-2A and FR-2B to Corsica flag per ISO standards
- FR-971, FR-973, FR-974, FR-976 changed to France flag as official per ISO 3166
- FR-972 changed from France to Martinique flag
- Removed several GB flags (COA and banners) that don't meet flag standards
- Added comprehensive notes section to each country subdivision markdown file

#### Project Structure
- Added `iso3166-flags-metadata` directory with comprehensive metadata
- Added stats section to main README
- Modified ISO 3166-2 CSS: removed country code prefix, only subdivision code in selectors
- Removed GB-UKM, GB-EAW, GB-GBN flags

#### Coverage
- ISO 3166-1: ✅ 250/250 countries (100% complete)
- ISO 3166-2: 🟡 ~2,200 subdivisions missing (~77% of 2,843 subdivisions need flags)

#### Data & Automation
- Implemented Python scripts for automated CSS generation, metadata export, and README generation
- Added GitHub Actions CI/CD pipeline with pytest integration
- Created quality scoring system for flag images (0-100 scale)
- Implemented image format conversion pipeline (WebP, GIF → PNG/SVG)

---

## Version Tags

When making releases, use semantic versioning:

- **MAJOR**: Breaking changes (e.g., CSS selector format changes, schema overhauls)
- **MINOR**: New flags added, new countries covered, non-breaking feature additions
- **PATCH**: Bug fixes, quality improvements, documentation updates

### Example Upcoming Tags
- `v2.0.0` - Major: CSS selector redesign or schema overhaul
- `v1.5.0` - Minor: 50+ new subdivision flags added
- `v1.4.2` - Patch: Bug fix in metadata calculation

---

## How to Contribute

When adding or modifying flags:

1. Add flag files to appropriate directory (`iso3166-1-flags/` or `iso3166-2-flags/<COUNTRY_CODE>/`)
2. Run `python scripts/update_everything.py --dry-run` to preview changes
3. Review generated CSS, metadata, and README files
4. Run `python scripts/update_everything.py` to finalize (creates full commit)
5. Update this CHANGELOG.md with changes in "Unreleased" section
6. Create pull request with clear description

## File Organization

- **`iso3166-1-flags/`** - Country flags (250 total, all complete)
- **`iso3166-2-flags/`** - Subdivision flags (partial coverage)
- **`iso3166-flags-metadata/`** - Generated metadata files
  - `iso3166_1_flag_metadata.csv` - Individual country flag metrics
  - `iso3166_2_flag_metadata.csv` - Individual subdivision flag metrics
  - `iso3166_flags_metadata.json` - Aggregate statistics
- **`css/`** - Auto-generated CSS stylesheets
  - `iso3166-1.css` - Country flag selectors
  - `iso3166-2.css` - Subdivision flag selectors
- **`scripts/`** - Python automation scripts
- **`tests/`** - Unit and integration test suite

## Contact & Support

For issues, questions, or flag submissions, please open a GitHub issue or pull request.

---

**Last Updated**: April 2026
**Maintained By**: @amckenna41
