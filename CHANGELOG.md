# devtoolkit Changelog

## [Unreleased]

- Add `python-tools/run.sh` launcher to create a local virtualenv and run the CLI or tests.
- Split runtime and dev dependencies into `requirements.txt` and `requirements-dev.txt`.
- Add test instructions and require running tests before PRs in `PULL_REQUEST_TEMPLATE.md`.
- Add GitHub Actions workflow to run Python tests on PRs.
- Update README files to document the launcher and running tests locally.

- Fix Raycast result field updates (use defaultValue + id/key remount pattern).
- Add smoke test script to verify Python CLI integration.
- Remove hard-coded absolute paths from TypeScript and VS Code settings.
- Update docs to prefer `defaultValue` for result fields.

## [Initial Version] - {PR_MERGE_DATE}