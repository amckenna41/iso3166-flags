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

### Fixed
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
