# ISO 3166-flags Workflows

* `build_test.yml` - build and test the iso3166-flags pipeline on every push/PR to `main`:
  * runs the unit tests on Python 3.10-3.12 and validates every SVG is well-formed XML;
  * checks the README Quick Stats table matches `iso3166-flags-metadata/iso3166_flags_metadata.json`;
  * fails if the committed CSS, sprite, README or metadata files are stale relative to the flag folders (`python -m scripts.update_everything --check`) - run `python3 scripts/update_everything.py` after adding/changing flags;
  * fails on any known vulnerability in the pinned requirements (`pip-audit`) or medium+ Bandit finding in `scripts/`;
  * runs flake8 and uploads a coverage report to Codecov.
* `check_upstream_flags.yml` - runs quarterly (and on demand) to sync `iso3166-1-flags` with the latest [lipis/flag-icons](https://github.com/lipis/flag-icons) release, opening a PR only when flags were added, updated or removed:
  * new upstream flags are only added if they're an official ISO 3166-1 alpha-2 code;
  * flags in the repo whose code isn't official (the curated reserved-code flags e.g. `ac`, `eu`, `uk`, `un`) are never overwritten or deleted.

All third-party actions are pinned to a commit SHA.
