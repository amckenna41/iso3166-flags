# ISO 3166-flags Workflows

* `build_test.yml` - build and test the iso3166-flags pipeline on every push/PR to `main`:
  * runs the unit tests on every supported Python version (3.10-3.14) and validates every SVG is well-formed XML;
  * fails if any SVG contains scripts, event handlers, remote references or references to elements missing from the file, a PNG/JPG's content doesn't match its extension, or an ISO 3166-2 flag isn't named after a real subdivision code of its country sub-folder (`python -m scripts.validate_flags`);
  * checks the README Quick Stats table matches `iso3166-flags-metadata/iso3166_flags_metadata.json`;
  * fails if the committed CSS, sprite, README or metadata files are stale relative to the flag folders (`python -m scripts.update_everything --check`) - run `python3 scripts/update_everything.py` after adding/changing flags;
  * reports known vulnerabilities in the pinned requirements (`pip-audit`) without failing the workflow, and fails on any medium+ Bandit finding in `scripts/`;
  * runs flake8 and uploads a coverage report to Codecov.
* `check_upstream_flags.yml` - runs quarterly (and on demand) to sync `iso3166-1-flags` with the latest [lipis/flag-icons](https://github.com/lipis/flag-icons) release, opening a PR only when flags were added, updated or removed:
  * the run is skipped if a PR for the same release is still open, or was merged and hasn't since been reverted;
  * new upstream flags are only added if they're an official ISO 3166-1 alpha-2 code;
  * flags in the repo whose code isn't official (the curated reserved-code flags e.g. `ac`, `eu`, `uk`, `un`) are never overwritten or deleted;
  * the derived CSS, README and metadata files are regenerated (`update_everything.py`) and included in the PR;
  * the synced flags must pass `validate_flags` and the unit tests, otherwise the run fails and no PR is opened. PRs opened with `GITHUB_TOKEN` don't trigger `build_test.yml`, so these are the only checks they get before review.

All third-party actions are pinned to a commit SHA, kept up to date by a monthly grouped Dependabot PR (`.github/dependabot.yml`).
