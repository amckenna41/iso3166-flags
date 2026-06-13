# Changelog

All notable changes to the **iso3166-flags** project are documented in this file. This project tracks changes to flag assets, metadata structures, and schema updates following ISO 3166-1 and ISO 3166-2 standards.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## []

### Added
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
